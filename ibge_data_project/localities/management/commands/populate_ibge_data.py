import requests
from django.core.management.base import BaseCommand
from localities.models import Region, State, City, District
import time

class Command(BaseCommand):
    help = 'Populates the database with data from the IBGE API'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando a população de dados da API do IBGE...'))

        # Adicionar uma função auxiliar para lidar com as requisições
        def make_request_with_retry(url, retries=5, timeout=30):
            for i in range(retries):
                try:
                    response = requests.get(url, timeout=timeout)
                    response.raise_for_status() # Lança um erro se a resposta for um status de erro HTTP
                    return response.json()
                except (requests.exceptions.RequestException) as e:
                    self.stdout.write(self.style.WARNING(f"Erro na requisição ({url}): {e}"))
                    if i < retries - 1:
                        wait_time = 2 ** i # Espera exponencial
                        self.stdout.write(f"Tentando novamente em {wait_time} segundos...")
                        time.sleep(wait_time)
                    else:
                        self.stdout.write(self.style.ERROR(f"Máximo de tentativas excedido para a URL: {url}"))
                        return None
        
        # 1. Popula as Regiões
        self.stdout.write('Buscando Regiões...')
        regions_data = make_request_with_retry('https://servicodados.ibge.gov.br/api/v1/localidades/regioes')

        if regions_data:
            regions_map = {
                r['id']: Region.objects.update_or_create(ibge_id=r['id'], defaults={'name': r['nome']})[0]
                for r in regions_data
            }
        else:
            self.stdout.write(self.style.ERROR('Falha ao obter dados de Regiões. Encerrando o processo.'))
            return

        # 2. Popula os Estados
        self.stdout.write('Buscando Estados...')
        states_data = make_request_with_retry('https://servicodados.ibge.gov.br/api/v1/localidades/estados')

        if states_data:
            for state_data in states_data:
                state, created = State.objects.update_or_create(
                    ibge_id=state_data['id'],
                    defaults={
                        'name': state_data['nome'],
                        'uf': state_data['sigla'],
                        'region': regions_map.get(state_data['regiao']['id'])
                    }
                )
                if created:
                    self.stdout.write(f'  Estado criado: {state.name}')

                # 3. Popula os Municípios
                cities_url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state.ibge_id}/municipios'
                cities_data = make_request_with_retry(cities_url)
                
                if cities_data:
                    for city_data in cities_data:
                        city, created = City.objects.update_or_create(
                            ibge_id=city_data['id'],
                            defaults={'name': city_data['nome'], 'state': state}
                        )
                        if created:
                            self.stdout.write(f'    Município criado: {city.name}')

                        # 4. Popula os Distritos
                        districts_url = f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{city.ibge_id}/distritos'
                        districts_data = make_request_with_retry(districts_url)

                        if districts_data:
                            for district_data in districts_data:
                                district, created = District.objects.update_or_create(
                                    ibge_id=district_data['id'],
                                    defaults={'name': district_data['nome'], 'city': city}
                                )
                                if created:
                                    self.stdout.write(f'      Distrito criado: {district.name}')
        
        self.stdout.write(self.style.SUCCESS('População de dados finalizada (com possíveis erros registrados).'))