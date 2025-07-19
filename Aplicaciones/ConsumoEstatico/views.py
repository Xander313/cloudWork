from django.shortcuts import render, redirect
from .models import ConsumoEstatico
from Aplicaciones.UsuarioSensor.models import UsuarioSensor
from django.contrib import messages

def editar_consumo_estatico(request, id):
    consumos = ConsumoEstatico.objects.filter(id=id)
    if not consumos.exists():
        messages.error(request, 'Consumo estático no encontrado.')
        return redirect('lista_consumo_estatico')
    consumo = consumos.first()
    if request.method == 'POST':
        try:
            consumo.consumoEstatico = float(request.POST.get('consumoEstatico'))
            consumo.save()
            messages.success(request, 'Lectura estática actualizado correctamente.')
            return redirect('lista_consumo_estatico')
        except Exception as e:
            messages.error(request, 'Error al actualizar: ' + str(e))
    consumo.consumoEstatico = str(consumo.consumoEstatico).replace(',', '.')
    return render(request, 'admin/editar_consumo_estatico.html', {'consumo': consumo})

def eliminar_consumo_estatico(request, id):
    consumos = ConsumoEstatico.objects.filter(id=id)
    if not consumos.exists():
        messages.error(request, 'Consumo estático no encontrado.')
        return redirect('lista_consumo_estatico')
    consumo = consumos.first()
    consumo.delete()
    messages.success(request, 'Consumo estático eliminado correctamente.')
    return redirect('lista_consumo_estatico')


def agregar_consumo_estatico(request):
    usados_ids = ConsumoEstatico.objects.values_list('usuarioSensor_id', flat=True)

    disponibles = UsuarioSensor.objects.exclude(id__in=usados_ids)

    return render(request, 'admin/agregar_consumo_estatico.html', {
        'usuariosSensoresDisponibles': disponibles
    })


