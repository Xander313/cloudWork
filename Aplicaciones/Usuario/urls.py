from django.urls import path
from . import views

urlpatterns = [


    
    ################ ESTA RUTA ES PARA EL MENU CENTRAL##############
    path('sesionIniciada/', views.menuCentral, name='menuCentral'), 

    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

    # Rutas para login y registro
    path('login/', views.login_view, name='login'),  # Asegúrate de que esta línea esté presente
    path('registro/', views.registro, name='registro'),
    path('verify_email/', views.verify_email, name='verify_email'),  # Ruta para verificación


]