from django.db import models


class Person(models.Model):
    Nombres = models.TextField(max_length=100, null=False, unique=True)
    Nombres2 = models.TextField(max_length=100, null=False)
    Genero = models.TextField(max_length=6, null=False)
    Probabilidad = models.FloatField()
    Frecuencia = models.FloatField()
    Pais = models.TextField(max_length=100, null=False)
    EdadMedia = models.FloatField()

    def __str__(self):
        return f'{self.Nombres}: {self.Genero}'




