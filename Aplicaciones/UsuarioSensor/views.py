# views.py en la aplicación UsuarioSensor
from django.shortcuts import render, redirect, get_object_or_404
from .models import UsuarioSensor
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Sensor.models import Sensor
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def panel_admin(request):
    if not request.session.get('es_admin'):
        return redirect('login')  # Redirige si no es admin

    usuarios = Usuario.objects.all()  # Obtener todos los usuarios
    sensores = Sensor.objects.all()  # Obtener todos los sensores
    asignaciones = UsuarioSensor.objects.all()  # Obtener todas las asignaciones

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario')
        sensor_id = request.POST.get('sensor')
        ubicacion = request.POST.get('ubicacion')

        # Crear una nueva asignación
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            sensor = Sensor.objects.get(id=sensor_id)
            asignacion = UsuarioSensor(usuario=usuario, sensor=sensor, ubicacionSensor=ubicacion)
            asignacion.save()
            messages.success(request, 'Sensor asignado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al asignar sensor: {str(e)}')

    return render(request, 'admin/paneladmin.html', {
        'usuarios': usuarios,
        'sensores': sensores,
        'asignaciones': asignaciones,
    })

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado exitosamente.')
    return redirect('panel_admin')




def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        correo = request.POST.get('correo')
        nombre = request.POST.get('nombre')
        password = request.POST.get('password')
        usuario.correoUsuario = correo         # <--- CAMBIA ESTO
        usuario.nombreUsuario = nombre         # <--- Y ESTO
        if password:
            usuario.passwordUsuario = make_password(password)  # <--- Y ESTO
        usuario.save()
        messages.success(request, 'Usuario actualizado correctamente.')
        return redirect('panel_admin')
    return render(request, 'admin/editar_usuario.html', {'usuario': usuario})