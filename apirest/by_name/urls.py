from django.urls import path

from by_name.views import Consulta

urlpatterns = [
    path('<name>', Consulta.as_view()),
]
