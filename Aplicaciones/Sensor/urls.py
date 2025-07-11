from django.urls import path
from .views import agregar_sensor, editar_sensor, eliminar_sensor

urlpatterns = [
    path('agregar_sensor/', agregar_sensor, name='agregar_sensor'),
    path('editar_sensor/<id>/', editar_sensor, name='editar_sensor'),
    path('eliminar_sensor/<id>/', eliminar_sensor, name='eliminar_sensor'),



]