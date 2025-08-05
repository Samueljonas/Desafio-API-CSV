import csv
from django.core.management.base import BaseCommand
from localities.models import Empresa
import os

class Command(BaseCommand):
    help = 'Importa dados de empresas de um arquivo CSV.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='O caminho para o arquivo CSV de empresas.')

    def handle(self, *args, **options):
        file_path = options['csv_file']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Arquivo não encontrado: {file_path}"))
            return

        self.stdout.write(self.style.SUCCESS('Iniciando a importação de dados de empresas...'))

        with open(file_path, 'r', encoding='latin-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')

            # A primeira linha é o cabeçalho, vamos pular ela.
            # Se o arquivo não tiver cabeçalho, remova a próxima linha.
            # next(reader)

            total_rows = sum(1 for row in csv.reader(open(file_path, 'r', encoding='latin-1'), delimiter=';')) - 1
            current_row = 0

            for row in reader:
                current_row += 1
                try:
                    cnpj_basico = row[0]
                    razao_social = row[1]
                    natureza_juridica = row[2]
                    qualificacao_responsavel = row[3]
                    capital_social = row[4]
                    porte_empresa = row[5]
                    ente_federativo_responsavel = row[6]

                    Empresa.objects.update_or_create(
                        cnpj_basico=cnpj_basico,
                        defaults={
                            'razao_social': razao_social,
                            'natureza_juridica': natureza_juridica,
                            'qualificacao_responsavel': qualificacao_responsavel,
                            'capital_social': capital_social,
                            'porte_empresa': porte_empresa,
                            'ente_federativo_responsavel': ente_federativo_responsavel,
                        }
                    )

                    if current_row % 1000 == 0:
                        self.stdout.write(f"Processando linha {current_row}/{total_rows}")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro na linha {current_row}: {e}"))
                    continue

        self.stdout.write(self.style.SUCCESS('Importação de dados de empresas finalizada com sucesso!'))
