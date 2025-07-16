from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import TipoMensaje

# Editar TipoMensaje
def editar_tipo_mensaje(request, id):
    tipo_mensaje = get_object_or_404(TipoMensaje, id=id)
    if request.method == 'POST':
        try:
            tipo_mensaje.tipoAlerta = request.POST.get('tipoAlerta')
            tipo_mensaje.mensaje_default = request.POST.get('mensaje_default')
            tipo_mensaje.save()
            messages.success(request, 'Tipo de mensaje actualizado correctamente.')
            return redirect('lista_tipo_mensaje')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {e}')
    return render(request, 'admin/editar_tipo_mensaje.html', {'tipo': tipo_mensaje})

# Eliminar TipoMensaje
def eliminar_tipo_mensaje(request, id):
    tipo_mensaje = get_object_or_404(TipoMensaje, id=id)
    tipo_mensaje.delete()
    messages.success(request, 'Tipo de mensaje eliminado correctamente.')
    return redirect('lista_tipo_mensaje')
