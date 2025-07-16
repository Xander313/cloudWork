from django.urls import path
from . import views


urlpatterns = [
    path('consumo_estatico/', views.lista_consumo_estatico, name='lista_consumo_estatico'),
    path('', views.IniciarSesion, name="IniciarSesion" ),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),

]
