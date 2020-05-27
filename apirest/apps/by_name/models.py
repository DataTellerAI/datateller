import pymongo
from django.db import models



# Create your models here.
class Person(models.Model):
    names = models.TextField(max_length=20, null=False)
    gende = models.CharField(max_length=1, null=False)


    def __str__(self):
        return self.names + self.gende
