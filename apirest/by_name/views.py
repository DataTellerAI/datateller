import pymongo
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from pymongo import MongoClient
from rest_framework.views import APIView


class Consulta(APIView):
    def get(self, request, name):
        print(name)

        client = MongoClient(
            "mongodb+srv://Campo:Campo1987@names-f54kh.mongodb.net/test?retryWrites=true&w=majority")
        _myDict = {}


        db = client.Names
        filter = {"Nombres": name}
        objs = db.genderName.find(filter)
        for obj in objs:
            MyObj = obj
        _myDict['Nombres'] = name
        _myDict['Genero'] = MyObj['Genero']
        _myDict['Pais'] = MyObj['Pais']
        return JsonResponse(_myDict)
