from django.urls import path
from . import views


urlpatterns = [
    path('', views.IniciarSesion, name="IniciarSesion" ),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),

]
