from django.shortcuts import render, redirect
from .models import LogUsuario
from django.contrib import messages

def eliminar_log_usuario(request, id):
    logs = LogUsuario.objects.filter(id=id)
    if not logs.exists():
        messages.error(request, 'Log de usuario no encontrado.')
        return redirect('ver_logs_usuario')
    log = logs.first()
    log.delete()
    messages.success(request, 'Log de usuario eliminado correctamente.')
    return redirect('ver_logs_usuario')

def editar_log_usuario(request, id):
    log = LogUsuario.objects.filter(id=id).first()
    if not log:
        messages.error(request, 'Log de usuario no encontrado.')
        return redirect('ver_logs_usuario')

    if request.method == 'POST':
        try:
            log.evento = request.POST.get('evento')
            log.usuario = request.POST.get('usuario')
            log.save()
            messages.success(request, 'Log de usuario actualizado correctamente.')
            return redirect('ver_logs_usuario')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {e}')
    
    return render(request, 'admin/editar_log_usuario.html', {'log': log})