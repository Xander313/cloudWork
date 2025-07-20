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

def lista_consumo_dinamico(request):
    consumos_dinamicos = ConsumoDinamico.objects.all()
    return render(request, 'admin/consumo_dinamico.html', {
        'consumos_dinamicos': consumos_dinamicos
    })

def lista_notificaciones(request):
    notificaciones = Notificacion.objects.all()
    return render(request, 'admin/notificaciones.html', {
        'notificaciones': notificaciones
    })

def lista_tipo_mensaje(request):
    tipo_mensajes = TipoMensaje.objects.all()
    return render(request, 'admin/tipo_mensajes.html', {
        'tipo_mensajes': tipo_mensajes
    })


def ver_logs_usuario(request):
    logs = LogUsuario.objects.all().order_by('-fechaCambio')

    return render(request, 'admin/log_usuario.html', {
        'logs': logs
    })

def lista_consumo_historico(request):
    consumos_historicos = ConsumoHistorico.objects.all()
    return render(request, 'admin/consumo_historico.html', {
        'consumos_historicos': consumos_historicos
    })
