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


# crear funcion para mostrar datos de todos los modelos
def panel_admi(request):
    notificaciones = Notificacion.objects.select_related('usuarioSensor__usuario', 'usuarioSensor__sensor', 'tipoMensaje').order_by('-fechaEnvio')
    consumos_estaticos = ConsumoEstatico.objects.all()
    consumos_historicos = ConsumoHistorico.objects.all()
    consumos_dinamicos = ConsumoDinamico.objects.all()
    logs_usuario = LogUsuario.objects.all()
    tipos_mensajes = TipoMensaje.objects.all()

    return render(request, 'admin/paneladmin.html', {
        'notificaciones': notificaciones,
        'consumos_estaticos': consumos_estaticos,
        'consumos_historicos': consumos_historicos,
        'consumos_dinamicos': consumos_dinamicos,
        'logs_usuario': logs_usuario,
        'tipos_mensajes': tipos_mensajes,
    })

