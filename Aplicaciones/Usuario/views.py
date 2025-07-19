from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import Usuario
import uuid
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import random
from django.db.models import ProtectedError
from django.core.files.storage import default_storage
import os
from Aplicaciones.LogsUsuario.models import LogUsuario  # Ajusta el path real a tu proyecto




# Create your views here.

from django.contrib.auth.hashers import make_password



def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correoUsuario')
        password = request.POST.get('passwordUsuario')

        if correo == 'admin' and password == '1234':
            request.session['es_admin'] = True
            return redirect('listaAsignacion')  

        try:
            usuario = Usuario.objects.get(correoUsuario=correo)

            if usuario.passwordUsuario == "":
                request.session['pendiente_password'] = usuario.id
                return render(request, 'iniciarSesion/login.html', {
                    'mostrar_modal': True,
                    'usuario_id': usuario.id
                })

            if check_password(password, usuario.passwordUsuario):
                request.session['usuario_id'] = usuario.id
                nombre_usuario = usuario.nombreUsuario


                # 👇 Registro en LogUsuario con los campos que definiste
                LogUsuario.objects.create(
                    evento='Inicio de sesión',
                    descripcion=f'El usuario {nombre_usuario} inició sesión correctamente.',
                    usuario=usuario
                )

                return render(request, 'Usuario/menucentral.html', {
                    'usuario_id': usuario.id,
                    'nombre_usuario': nombre_usuario
                })

            else:
                messages.error(request, 'Contraseña incorrecta')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'iniciarSesion/login.html')





def establecer_password(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        nueva_pass = request.POST.get('nueva_password')

        try:
            usuario = Usuario.objects.get(id=usuario_id)
            usuario.passwordUsuario = make_password(nueva_pass)
            usuario.save()

            # ✅ Registrar en el log
            LogUsuario.objects.create(
                evento='Inicio de sesión',
                descripcion=f'El usuario {usuario.nombreUsuario} configuró su contraseña e inició sesión.',
                usuario=usuario
            )

            messages.success(request, 'Contraseña configurada correctamente.')
            request.session['usuario_id'] = usuario.id
            return render(request, 'Usuario/menucentral.html', {
                'usuario_id': usuario.id,
                'nombre_usuario': usuario.nombreUsuario
            })
        except Usuario.DoesNotExist:
            messages.error(request, 'Error al configurar contraseña.')
            return redirect('login')











def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreUsuario')  # <-- Nuevo
        correo = request.POST.get('correoUsuario')
        password = request.POST.get('passwordUsuario')
        
        verification_code = random.randint(100000, 999999)
        
        send_mail(
            'Código de Verificación',
            f'Tu código de verificación es: {verification_code}',
            'tu_correo@example.com',
            [correo],
            fail_silently=False,
        )
        
        request.session['verification_code'] = verification_code
        request.session['correo'] = correo
        request.session['password'] = password
        request.session['nombre'] = nombre  # <-- Nuevo
        
        messages.success(request, 'Se ha enviado un código de verificación a tu correo electrónico.')
        return redirect('verify_email')
    return render(request, 'iniciarSesion/login.html', {'show_register': True})

def verify_email(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        if verification_code == str(request.session.get('verification_code')):
            correo = request.session.get('correo')
            password = request.session.get('password')
            nombre = request.session.get('nombre')  # <-- Nuevo
            if not Usuario.objects.filter(correoUsuario=correo).exists():
                usuario = Usuario(
                    nombreUsuario=nombre,  # <-- Cambiado
                    correoUsuario=correo,
                    passwordUsuario=make_password(password)
                )
                usuario.save()
                messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            else:
                messages.info(request, 'El usuario ya existe. Inicia sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Código de verificación incorrecto. Intenta de nuevo.')
    return render(request, 'iniciarSesion/verify.html')

# no tocar
def perfil_usuario(request):
    return render(request, 'Usuario/perfil.html')


    
def menuCentral(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        request.session['usuario_id'] = usuario_id
    else:
        usuario_id = request.session.get('usuario_id')
    
    nombre_usuario = None
    if usuario_id:
        try:
            nombre_usuario = Usuario.objects.get(id=usuario_id).nombreUsuario
        except Usuario.DoesNotExist:
            pass
    print (nombre_usuario)
    
    return render(request, 'Usuario/menucentral.html', {
        'usuario_id': usuario_id,
        'nombre_usuario': nombre_usuario
    })




def lista_usuario(request):
    if not request.session.get('es_admin'):
        return redirect('login') 

    usuarios = Usuario.objects.all()  

    return render(request, 'Usuario/index.html', {
        'usuarios': usuarios,

    })




def agregar_usuario(request):
    if not request.session.get('es_admin'):
        return redirect('login')

    correos_existentes = list(Usuario.objects.values_list('correoUsuario', flat=True))
    telefonos_existentes = list(Usuario.objects.values_list('telefonoUsuario', flat=True))


    if request.method == 'POST':
        correo = request.POST.get('correo')
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono', '')
        direccion = request.POST.get('direccion', '')
        foto = request.FILES.get('fotoPerfil') 

        if correo in correos_existentes:
            messages.error(request, 'Ya existe un usuario con ese correo.')
            return render(request, 'Usuario/agregar_usuario.html', {
                'correos': correos_existentes,
                'correo': correo,
                'nombre': nombre,
                'telefono': telefono,
                'direccion': direccion
            })
        if telefono in telefonos_existentes and telefono != '':
            messages.error(request, 'Ya existe un usuario con ese teléfono.')
            return render(request, 'Usuario/agregar_usuario.html', {
                'correos': correos_existentes,
                'telefonos': telefonos_existentes,
                'correo': correo,
                'nombre': nombre,
                'telefono': telefono,
                'direccion': direccion
            })


        Usuario.objects.create(
            nombreUsuario=nombre,
            correoUsuario=correo,
            telefonoUsuario=telefono,
            direccionUsuario=direccion,
            passwordUsuario="",
            fotoPerfil=foto
        )
        messages.success(request, 'Usuario registrado correctamente.')
        return redirect('lista_usuario')

    return render(request, 'Usuario/agregar_usuario.html', {
        'correos': correos_existentes,
        'telefonos': telefonos_existentes,
    })







def editar_usuario(request, usuario_id):
    if not request.session.get('es_admin'):
        return redirect('login') 
    usuario = get_object_or_404(Usuario, id=usuario_id)

    correos_existentes = list(Usuario.objects.values_list('correoUsuario', flat=True))
    telefonos_existentes = list(Usuario.objects.values_list('telefonoUsuario', flat=True))

    if request.method == 'POST':
        correo = request.POST.get('correo')
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono', '')
        direccion = request.POST.get('direccion', '')
        password = request.POST.get('password')
        eliminar = request.POST.get('eliminar_password')
        nueva_foto = request.FILES.get('fotoPerfil')

        if nueva_foto:
            if usuario.fotoPerfil and default_storage.exists(usuario.fotoPerfil.name):
                default_storage.delete(usuario.fotoPerfil.name)

            usuario.fotoPerfil = nueva_foto

        if Usuario.objects.filter(correoUsuario=correo).exclude(id=usuario_id).exists():
            messages.error(request, 'Ya existe un usuario con ese correo.')
            return render(request, 'Usuario/editar_usuario.html', {
                'usuario': usuario,
                'correo': correo,
                'nombre': nombre,
                'telefono': telefono,
                'direccion': direccion
            })

        usuario.correoUsuario = correo
        usuario.nombreUsuario = nombre
        usuario.telefonoUsuario = telefono
        usuario.direccionUsuario = direccion

        if eliminar == 'true':
            usuario.passwordUsuario = ""

        elif password:
            usuario.passwordUsuario = make_password(password)

        usuario.save()
        messages.success(request, 'Usuario actualizado correctamente.')
        return redirect('lista_usuario')


    return render(request, 'Usuario/editar_usuario.html', {
        'usuario': usuario,
        'correos': correos_existentes,
        'telefonos': telefonos_existentes,
        'correo_actual': usuario.correoUsuario,
        'telefono_actual': usuario.telefonoUsuario
    })



def eliminar_usuario(request, usuario_id):
    if not request.session.get('es_admin'):
        return redirect('login') 
    usuario = get_object_or_404(Usuario, id=usuario_id)

    try:
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
    except ProtectedError:
        messages.error(request, 'No se puede eliminar este usuario porque tiene datos asociados.')

    return redirect('lista_usuario')
