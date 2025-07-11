from django.shortcuts import render, get_object_or_404, redirect
from Aplicaciones.Usuario.models import Usuario
from django.http import JsonResponse
from Aplicaciones.Notificaciones.models import Notificacion
from django.utils.timezone import localtime
from Aplicaciones.ConsumoHistorico.models import ConsumoHistorico
from Aplicaciones.UsuarioSensor.models import UsuarioSensor
from django.contrib import messages


def ver_notificaciones_por_usuario(request, id):
    usuario_id = request.session['usuario_id']
    usuario = get_object_or_404(Usuario, pk=id)
    sensores = UsuarioSensor.objects.filter(usuario=usuario)
    
    return render(request, 'Notificaciones/panelNotificaciones.html', {
        'usuario': usuario,
        'sensores': sensores,
        'usuario_id': usuario_id
    })



def obtener_notificaciones_sensor(request, sensor_id):
    notificaciones = Notificacion.objects.filter(usuarioSensor__id=sensor_id).order_by('-fechaEnvio')
    
    data = [
        {
            'mensaje': n.mensaje,
            'fechaEnvio': localtime(n.fechaEnvio).strftime("%Y-%m-%d %H:%M"), 
            'tipo': n.tipoMensaje.tipoAlerta
        }
        for n in notificaciones
    ]
    
    return JsonResponse({'notificaciones': data})


def estadisticaPresenracion(request, id):
    
    usuario = get_object_or_404(Usuario, pk=id)
    sensores_asignados = UsuarioSensor.objects.filter(usuario=usuario)

    sensores_con_config = []

    for sensor in sensores_asignados:
        sensores_con_config.append({
            'id': sensor.id,
            'sensor': sensor.sensor,
            'ubicacionSensor': sensor.ubicacionSensor,
        })

    return render(request, 'estadisticas/estaditicaPrevio.html', {
        'sensores': sensores_con_config,
        'usuario_id': usuario.id,
    })



def reporte_consumo_json(request, sensor_id):
    historico = ConsumoHistorico.objects.filter(usuarioSensor_id=sensor_id).order_by('fechaPeriodo')

    datos = {
        "fechas": [h.fechaPeriodo.strftime('%d/%m') for h in historico],
        "consumo_total": [h.consumoTotal for h in historico],
        "maximo": [h.maxConsumo for h in historico],
        "promedio": [h.minConsumo for h in historico], 
    }

    return JsonResponse(datos)


def reporte_consumo_pie(request, sensor_id):
    historico = (
        ConsumoHistorico.objects
        .filter(usuarioSensor_id=sensor_id)
        .order_by('-fechaPeriodo')[:7]
    )

    historico = list(historico)[::-1]

    dias_en = [h.fechaPeriodo.strftime('%A') for h in historico]
    
    dias_traducidos = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }

    dias_es = [dias_traducidos.get(dia, dia) for dia in dias_en]
    consumos = [h.consumoTotal for h in historico]

    return JsonResponse({
        "dias": dias_es,
        "consumos": consumos
    })



def eliminar_notificacion(request, id):
    notificaciones = Notificacion.objects.filter(id=id)
    if not notificaciones.exists():
        messages.error(request, 'Notificación no encontrada.')
        return redirect('panel_admin')
    notificacion = notificaciones.first()
    notificacion.delete()
    messages.success(request, 'Notificación eliminada correctamente.')
    return redirect('panel_admin')
