import json
from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'Nombres',
            'Nombres2',
            'Genero',
            'Probabilidad',
            'Frecuencia',
            'EdadMedia',
            'Pais',
        )


with open('/home/adru/Documents/Holberton/datateller/apirest/apps/by_name/nombres.JSON') as file:
    json_list = json.load(file)
for i in json_list:
    x = PersonSerializer(data=i)
    if x.is_valid():
        x.save()
    else:
        print(x.errors)
print('serializado')
