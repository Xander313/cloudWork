from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
def IniciarSesion(request):
    return render(request, 'iniciarSesion/login.html')

def cerrar_sesion(request):
    # Lógica para cerrar sesión
    logout(request)  # Asegúrate de importar logout desde django.contrib.auth
    return redirect('login')  # Redirige a donde desees