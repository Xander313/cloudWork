from django.shortcuts import render, redirect
from .models import ConsumoDinamico
from django.contrib import messages

def editar_consumo_dinamico(request, id):
    consumos = ConsumoDinamico.objects.filter(id=id)
    if not consumos.exists():
        messages.error(request, 'Consumo dinámico no encontrado.')
        return redirect('panel_admin')
    consumo = consumos.first()
    if request.method == 'POST':
        try:
            consumo.consumoDinamico = float(request.POST.get('consumoDinamico'))
            consumo.save()
            messages.success(request, 'Consumo dinámico actualizado correctamente.')
            return redirect('panel_admin')
        except Exception as e:
            messages.error(request, 'Error al actualizar: ' + str(e))
    return render(request, 'admin/editar_consumo_dinamico.html', {'consumo': consumo})

def eliminar_consumo_dinamico(request, id):
    consumos = ConsumoDinamico.objects.filter(id=id)
    if not consumos.exists():
        messages.error(request, 'Consumo dinámico no encontrado.')
        return redirect('panel_admin')
    consumo = consumos.first()
    consumo.delete()
    messages.success(request, 'Consumo dinámico eliminado correctamente.')
    return redirect('panel_admin')