from django.shortcuts import render, redirect
from django.contrib.auth import logout
from Aplicaciones.Notificaciones.models import Notificacion

from Aplicaciones.ConsumoEstatico.models import ConsumoEstatico
from Aplicaciones.ConsumoHistorico.models import ConsumoHistorico
from Aplicaciones.consumoDinamico.models import ConsumoDinamico
from Aplicaciones.LimiteUsuario.models import LimiteUsuario
from Aplicaciones.LogsUsuario.models import LogUsuario
from Aplicaciones.TipoMensaje.models import TipoMensaje


# Create your views here.
def IniciarSesion(request):
    return render(request, 'iniciarSesion/login.html')

def cerrar_sesion(request):
    # Lógica para cerrar sesión
    logout(request)  # Asegúrate de importar logout desde django.contrib.auth
    return redirect('login')  # Redirige a donde desees




def lista_consumo_estatico(request):
    consumos_estaticos = ConsumoEstatico.objects.all()
    return render(request, 'admin/consumo_estatico.html', {
        'consumos_estaticos': consumos_estaticos
    })

