from django.urls import path

from .views import Consulta

urlpatterns = [
    path('<name>', Consulta.as_view()),
]
