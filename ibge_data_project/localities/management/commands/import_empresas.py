import csv
from django.core.management.base import BaseCommand
from localities.models import Empresa
import os

class Command(BaseCommand):
    help = 'Importa dados de empresas de um arquivo CSV em lotes para maior desempenho.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='O caminho para o arquivo CSV de empresas.')

    def handle(self, *args, **options):
        file_path = options['csv_file']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Arquivo não encontrado: {file_path}"))
            return

        self.stdout.write(self.style.SUCCESS('Iniciando a importação em massa de dados de empresas...'))
        
        # Define o tamanho do lote para a inserção em massa
        batch_size = 5000
        empresa_objects = []
        with open(file_path, 'r', encoding='latin-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for i, row in enumerate(reader):
                try:
                    # Cria o objeto Empresa, mas não o salva ainda
                    empresa = Empresa(
                        cnpj_basico=row[0],
                        razao_social=row[1],
                        natureza_juridica=row[2],
                        qualificacao_responsavel=row[3],
                        capital_social=row[4],
                        porte_empresa=row[5],
                        ente_federativo_responsavel=row[6],
                    )
                    empresa_objects.append(empresa)

                    # Quando o lote atinge o tamanho definido, insere no banco
                    if len(empresa_objects) >= batch_size:
                        Empresa.objects.bulk_create(empresa_objects, ignore_conflicts=True)
                        self.stdout.write(f"Linhas {i - batch_size + 2} a {i + 1} importadas em massa.")
                        empresa_objects = []

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro na linha {i + 1}: {e}"))
                    continue

            # Salva os objetos restantes no último lote
            if empresa_objects:
                Empresa.objects.bulk_create(empresa_objects, ignore_conflicts=True)
                self.stdout.write(self.style.SUCCESS(f"Últimas {len(empresa_objects)} linhas importadas em massa."))

        self.stdout.write(self.style.SUCCESS('Importação de dados de empresas finalizada com sucesso!'))