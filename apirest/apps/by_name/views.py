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
            "mongodb+srv://backend:Seguridad1234@datateller1-clzfs.mongodb.net/test?retryWrites=true&w=majority")
        _myDict = {}
        db = client.datateller
        filter = {"Nombres": name}
        objs = db.namesdb.find(filter)
        for obj in objs:
            MyObj = obj
        _myDict['Nombres'] = name
        _myDict['Genero'] = MyObj['Genero']
        _myDict['Pais'] = MyObj['Pais']
        return JsonResponse(_myDict)
