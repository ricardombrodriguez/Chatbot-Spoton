from django.db import models

# Create your models here.
class Airport(models.Model):
    atributo = models.CharField(max_length=100)

class Flight(models.Model):
    ico24 = models.CharField()

