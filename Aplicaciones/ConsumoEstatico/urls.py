from django.urls import path
from .views import editar_consumo_estatico, eliminar_consumo_estatico

urlpatterns = [
    path('editar_consumo_estatico/<int:id>/', editar_consumo_estatico, name='editar_consumo_estatico'),
    path('eliminar_consumo_estatico/<int:id>/', eliminar_consumo_estatico, name='eliminar_consumo_estatico'),
]