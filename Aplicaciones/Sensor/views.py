from django.shortcuts import render, redirect
from .models import Sensor
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import ProtectedError







def lista_sensor(request):
    if not request.session.get('es_admin'):
        return redirect('login') 

    sensores = Sensor.objects.all() 


    return render(request, 'sensores/index.html', {
        'sensores': sensores,
    })



def agregar_sensor(request):
    if request.method == 'POST':
        sensorID = request.POST.get('sensorID')
        nombreSensor = request.POST.get('nombreSensor')
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')

        try:
            latitud = float(latitud)
            longitud = float(longitud)
        except (TypeError, ValueError):
            messages.error(request, 'Coordenadas inválidas.')
            return redirect('agregar_sensor')  

        nuevo_medidor = Sensor(
            sensorID=sensorID,
            nombreSensor=nombreSensor,
            latitud=latitud,
            longitud=longitud
        )
        nuevo_medidor.save()

        messages.success(request, 'Medidor de agua registrado correctamente.')
        return redirect('panel_admin')

    return render(request, 'sensores/agregar_sensor.html')



def editar_sensor(request, sensorID):
    try:
        sensor = Sensor.objects.get(sensorID=sensorID)
    except Sensor.DoesNotExist:
        messages.error(request, 'Medidor no encontrado.')
        return redirect('panel_admin')

    if request.method == 'POST':
        sensor.nombreSensor = request.POST.get('nombreSensor')

        # Captura coordenadas desde el formulario
        lat = request.POST.get('latitud')
        print(lat)
        lng = request.POST.get('longitud')
        print(lng)
        lat = lat.replace(',', '.')
        lng = lng.replace(',', '.')
        sensor.latitud = float(lat)
        sensor.longitud = float(lng)
        try:
            sensor.latitud = float(lat)
            sensor.longitud = float(lng)
        except (TypeError, ValueError):
            messages.error(request, 'Las coordenadas no son válidas.')
            return redirect('editar_sensor', sensorID=sensorID)

        sensor.save()
        messages.success(request, 'Medidor actualizado correctamente.')
        return redirect('panel_admin')

    return render(request, 'sensores/editar_sensor.html', {'sensor': sensor})

def eliminar_sensor(request, sensorID):
    sensores = Sensor.objects.filter(sensorID=sensorID)
    if not sensores.exists():
        messages.error(request, 'Sensor no encontrado.')
        return redirect('lista_sensor')

    sensor = sensores.first()

    try:
        sensor.delete()
        messages.success(request, 'Sensor eliminado correctamente.')
    except ProtectedError:
        messages.error(request, 'No se puede eliminar este medidor porque tiene datos asociados.')

    return redirect('lista_sensor')
