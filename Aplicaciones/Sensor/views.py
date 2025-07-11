from django.shortcuts import render, redirect
from .models import Sensor
from django.contrib import messages

def agregar_sensor(request):
    if request.method == 'POST':
        sensorID = request.POST.get('sensorID')
        nombreSensor = request.POST.get('nombreSensor')

        # Crear un nuevo sensor
        nuevo_sensor = Sensor(sensorID=sensorID, nombreSensor=nombreSensor)
        nuevo_sensor.save()

        messages.success(request, 'Sensor agregado correctamente.')
        return redirect('panel_admin')  # Cambia esto por la vista a la que deseas redirigir

    return render(request, 'admin/agregar_sensor.html')  # Usa el template correcto


def editar_sensor(request, sensorID):
    sensores = Sensor.objects.filter(sensorID=sensorID)
    if not sensores.exists():
        messages.error(request, 'Sensor no encontrado.')
        return redirect('panel_admin')
    sensor = sensores.first()
    if request.method == 'POST':
        sensor.nombreSensor = request.POST.get('nombreSensor')
        sensor.save()
        messages.success(request, 'Sensor actualizado correctamente.')
        return redirect('panel_admin')
    return render(request, 'admin/editar_sensor.html', {'sensor': sensor})

def eliminar_sensor(request, sensorID):
    sensores = Sensor.objects.filter(sensorID=sensorID)
    if not sensores.exists():
        messages.error(request, 'Sensor no encontrado.')
        return redirect('panel_admin')
    sensor = sensores.first()
    sensor.delete()
    messages.success(request, 'Sensor eliminado correctamente.')
    return redirect('panel_admin')