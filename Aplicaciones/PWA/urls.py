from django.urls import path
from . import views


urlpatterns = [
    path('notificaciones/', views.lista_notificaciones, name='lista_notificaciones'),
    path('consumo_estatico/', views.lista_consumo_estatico, name='lista_consumo_estatico'),
    path('consumo_dinamico/', views.lista_consumo_dinamico, name='lista_consumo_dinamico'),
    path('', views.IniciarSesion, name="IniciarSesion" ),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),

]
