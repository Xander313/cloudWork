from django.urls import path
from .views import editar_tipo_mensaje, eliminar_tipo_mensaje

urlpatterns = [
    path('editar/<int:id>/', editar_tipo_mensaje, name='editar_tipo_mensaje'),
    path('eliminar/<int:id>/', eliminar_tipo_mensaje, name='eliminar_tipo_mensaje'),
]
