from django.urls import path
from .views import eliminar_log_usuario

urlpatterns = [
    path('eliminar_log_usuario/<int:id>/', eliminar_log_usuario, name='eliminar_log_usuario'),
]