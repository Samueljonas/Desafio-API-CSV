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

