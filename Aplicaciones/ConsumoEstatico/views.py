from django.shortcuts import render, redirect
from .models import ConsumoEstatico
from django.contrib import messages

def editar_consumo_estatico(request, id):
    consumos = ConsumoEstatico.objects.filter(id=id)
    if not consumos.exists():
        messages.error(request, 'Consumo estático no encontrado.')
        return redirect('panel_admin')
    consumo = consumos.first()
    if request.method == 'POST':
        try:
            consumo.consumoEstatico = float(request.POST.get('consumoEstatico'))
            consumo.save()
            messages.success(request, 'Consumo estático actualizado correctamente.')
            return redirect('panel_admin')
        except Exception as e:
            messages.error(request, 'Error al actualizar: ' + str(e))
    return render(request, 'admin/editar_consumo_estatico.html', {'consumo': consumo})

def eliminar_consumo_estatico(request, id):
    consumos = ConsumoEstatico.objects.filter(id=id)
    if not consumos.exists():
        messages.error(request, 'Consumo estático no encontrado.')
        return redirect('panel_admin')
    consumo = consumos.first()
    consumo.delete()
    messages.success(request, 'Consumo estático eliminado correctamente.')
    return redirect('panel_admin')