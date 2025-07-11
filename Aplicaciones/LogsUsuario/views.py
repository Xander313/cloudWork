from django.shortcuts import render, redirect
from .models import LogUsuario
from django.contrib import messages

def eliminar_log_usuario(request, id):
    logs = LogUsuario.objects.filter(id=id)
    if not logs.exists():
        messages.error(request, 'Log de usuario no encontrado.')
        return redirect('panel_admin')
    log = logs.first()
    log.delete()
    messages.success(request, 'Log de usuario eliminado correctamente.')
    return redirect('panel_admin')