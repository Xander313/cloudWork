from django.urls import path
from .views import panel_admin, eliminar_usuario, editar_usuario

urlpatterns = [
    path('paneladmin/', panel_admin, name='panel_admin'),
    path('eliminar_usuario/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),
    path('editar_usuario/<int:usuario_id>/', editar_usuario, name='editar_usuario'),
]
