from django.shortcuts import render, get_object_or_404, redirect
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Sensor.models import Sensor
from Aplicaciones.UsuarioSensor.models import UsuarioSensor
from Aplicaciones.LimiteUsuario.models import LimiteUsuario
from Aplicaciones.ConsumoEstatico.models import ConsumoEstatico
from Aplicaciones.consumoDinamico.models import ConsumoDinamico
from django.contrib import messages

from django.utils import timezone





def presentar_limite_usuario(request, id):
    usuario_id = request.session['usuario_id']
    usuario = get_object_or_404(Usuario, pk=id)
    sensores_asignados = UsuarioSensor.objects.filter(usuario=usuario)

    sensores_con_config = []

    for sensor in sensores_asignados:
        # Buscar la última medición base registrada
        try:
            consumo_estatico = ConsumoEstatico.objects.filter(usuarioSensor=sensor).latest('fechaCorte')
            medicion_base = consumo_estatico.consumoEstatico
        except ConsumoEstatico.DoesNotExist:
            medicion_base = ''

        # Buscar configuración de límites
        try:
            limite = LimiteUsuario.objects.filter(usuarioSensor=sensor).latest('fechaCambio')
        except LimiteUsuario.DoesNotExist:
            limite = None

        sensores_con_config.append({
            'id': sensor.id,
            'sensor': sensor.sensor,
            'ubicacionSensor': sensor.ubicacionSensor,
            'medicionBase': medicion_base,
            'limiteDiario': limite.limiteDiario if limite else '',
            'umbralAlerta': limite.umbralAlerta if limite else '',
            'tiempoMinutos': limite.tiempoMinutos if limite else '',
        })

    return render(request, 'LimiteUsuario/configuraciones.html', {
        'sensores': sensores_con_config,
        'usuario_id': usuario.id
    })



def crearNuevoUsuarioSesor(request, id):
    usuario = get_object_or_404(Usuario, pk=id)

    if request.method == 'POST':
        sensor_id = request.POST.get('sensor_id')
        ubicacion = request.POST.get('ubicacion')
        medicion_base = request.POST.get('medicionBase').replace(',','.')
        limite_diario = request.POST.get('limiteDiario').replace(',','.')
        umbral_alerta = request.POST.get('umbralAlerta').replace(',','.')
        tiempo_minutos = request.POST.get('tiempo').replace(',','.')

        try:
            sensor = Sensor.objects.get(sensorID=sensor_id)
        except Sensor.DoesNotExist:
            print(f"❌ Sensor con ID único '{sensor_id}' no encontrado.")

            messages.error(request, "El sensor ingresado no está registrado.")

            sensores_asignados = UsuarioSensor.objects.filter(usuario=usuario)
            limites = LimiteUsuario.objects.filter(usuarioSensor__usuario=usuario)

            return render(request, 'LimiteUsuario/configuraciones.html', {
                'usuario': usuario,
                'id': usuario.id,
                'sensores': sensores_asignados,
                'limites': limites
            })

        usuario_sensor = UsuarioSensor.objects.create(
            usuario=usuario,
            sensor=sensor,
            ubicacionSensor=ubicacion
        )

        ConsumoEstatico.objects.create(
            usuarioSensor=usuario_sensor,
            consumoEstatico=medicion_base,
            fechaCorte=timezone.now()
        )

        LimiteUsuario.objects.create(
            usuarioSensor=usuario_sensor,
            limiteDiario=limite_diario,
            umbralAlerta=umbral_alerta,
            tiempoMinutos=tiempo_minutos
        )

        messages.success(request, 'Sensor asignado correctamente.')
        return redirect('presentar_limite_usuario', id=usuario.id)

    return redirect('presentar_limite_usuario', id=usuario.id)



def editar_usuario_sensor(request, id):
    usuario_sensor = get_object_or_404(UsuarioSensor, pk=id)
    
    if request.method == 'POST':
        # Leer los datos del formulario
        ubicacion = request.POST.get('ubicacion')
        medicion_base = request.POST.get('medicionBase').replace(',','.')
        limite_diario = request.POST.get('limiteDiario').replace(',','.')
        umbral_alerta = request.POST.get('umbralAlerta').replace(',','.')
        tiempo_minutos = request.POST.get('tiempo').replace(',','.')

        # Actualizar la ubicación en UsuarioSensor
        usuario_sensor.ubicacionSensor = ubicacion
        usuario_sensor.save()

        # Crear un nuevo registro en ConsumoEstatico si hay medición base
        if medicion_base:
            ConsumoEstatico.objects.create(
                usuarioSensor=usuario_sensor,
                consumoEstatico=medicion_base
            )

        # Obtener el último límite registrado para este usuarioSensor
        limite = LimiteUsuario.objects.filter(usuarioSensor=usuario_sensor).order_by('-fechaCambio').first()
        if limite:
            # Actualizar el último registro
            limite.limiteDiario = limite_diario
            limite.umbralAlerta = umbral_alerta
            limite.tiempoMinutos = tiempo_minutos
            limite.save()
        else:
            # Crear nuevo si no existe ninguno
            LimiteUsuario.objects.create(
                usuarioSensor=usuario_sensor,
                limiteDiario=limite_diario,
                umbralAlerta=umbral_alerta,
                tiempoMinutos=tiempo_minutos
            )

        messages.success(request, 'Configuración actualizada correctamente.')
        return redirect('presentar_limite_usuario', id=usuario_sensor.usuario.id)

    # Si es GET, puedes mostrar un template opcional (aunque usas modal JS)
    return render(request, 'LimiteUsuario/editar_sensor.html', {
        'sensor': usuario_sensor,
    })




def eliminar_usuario_sensor(request, id):
    usuario_sensor = get_object_or_404(UsuarioSensor, pk=id)
    usuario_id = usuario_sensor.usuario.id

    ConsumoEstatico.objects.filter(usuarioSensor=usuario_sensor).delete()
    LimiteUsuario.objects.filter(usuarioSensor=usuario_sensor).delete()
    ConsumoDinamico.objects.filter(usuarioSensor=usuario_sensor).delete()

    usuario_sensor.delete()

    messages.success(request, "Sensor y datos asociadas eliminadas correctamente.")
    return redirect('presentar_limite_usuario', id=usuario_id)