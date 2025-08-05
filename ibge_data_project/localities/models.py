from django.db import models

class Region(models.Model):
    ibge_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class State(models.Model):
    ibge_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='states')
    
    def __str__(self):
        return f"{self.name} ({self.uf})"
class City(models.Model):
    ibge_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")
    
    def __str__(self):
        return self.name
    
class District(models.Model):
    ibge_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.name

class Empresa(models.Model):
    """
    Modelo para representar os dados das empresas.
    Baseado no layout do arquivo "Empresas" do CNPJ.
    """
    cnpj_basico = models.CharField(max_length=8, unique=True, primary_key=True)
    razao_social = models.CharField(max_length=200, null=True, blank=True)
    natureza_juridica = models.CharField(max_length=4, null=True, blank=True)
    qualificacao_responsavel = models.CharField(max_length=2, null=True, blank=True)
    capital_social = models.CharField(max_length=20, null=True, blank=True)
    porte_empresa = models.CharField(max_length=2, null=True, blank=True)
    ente_federativo_responsavel = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.razao_social} ({self.cnpj_basico})"
