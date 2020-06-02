import json

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from .models import Person


class Consulta(APIView):
    def get(self, request, name):
        person = Person.objects.get(Nombres=name).__dict__
        del person['_state']
        return JsonResponse(person)
