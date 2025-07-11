from django.shortcuts import render, redirect
from .models import ConsumoHistorico
from django.contrib import messages

def editar_consumo_historico(request, id):
    historicos = ConsumoHistorico.objects.filter(id=id)
    if not historicos.exists():
        messages.error(request, 'Consumo histórico no encontrado.')
        return redirect('panel_admin')
    historico = historicos.first()
    if request.method == 'POST':
        try:
            historico.consumoTotal = float(request.POST.get('consumoTotal'))
            historico.maxConsumo = float(request.POST.get('maxConsumo'))
            historico.minConsumo = float(request.POST.get('minConsumo'))
            historico.fechaPeriodo = request.POST.get('fechaPeriodo')
            historico.save()
            messages.success(request, 'Consumo histórico actualizado correctamente.')
            return redirect('panel_admin')
        except Exception as e:
            messages.error(request, 'Error al actualizar: ' + str(e))
    return render(request, 'admin/editar_consumo_historico.html', {'historico': historico})

def eliminar_consumo_historico(request, id):
    historicos = ConsumoHistorico.objects.filter(id=id)
    if not historicos.exists():
        messages.error(request, 'Consumo histórico no encontrado.')
        return redirect('panel_admin')
    historico = historicos.first()
    historico.delete()
    messages.success(request, 'Consumo histórico eliminado correctamente.')
    return redirect('panel_admin')