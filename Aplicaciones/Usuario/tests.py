from django.test import TestCase, Client
from django.urls import reverse
from .models import Usuario
from django.contrib.auth.hashers import make_password

class UsuarioModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nombreUsuario='Juan Pérez',
            correoUsuario='juan@example.com',
            passwordUsuario=make_password('secreto123')
        )

    def test_creacion_usuario(self):
        usuario = Usuario.objects.get(correoUsuario='juan@example.com')
        self.assertEqual(usuario.nombreUsuario, 'Juan Pérez')

    def test_str_usuario(self):
        self.assertEqual(str(self.usuario), 'Juan Pérez')

    def test_actualizar_usuario(self):
        self.usuario.nombreUsuario = 'Juan Actualizado'
        self.usuario.save()
        self.assertEqual(Usuario.objects.get(pk=self.usuario.pk).nombreUsuario, 'Juan Actualizado')

    def test_eliminar_usuario(self):
        pk = self.usuario.pk
        self.usuario.delete()
        self.assertFalse(Usuario.objects.filter(pk=pk).exists())

class UsuarioViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(
            nombreUsuario='Test User',
            correoUsuario='testuser@example.com',
            passwordUsuario=make_password('testpass123')
        )

    def test_login_view_usuario_correcto(self):
        response = self.client.post(reverse('login'), {
            'correoUsuario': 'testuser@example.com',
            'passwordUsuario': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Usuario/menucentral.html')

    def test_login_view_usuario_incorrecto(self):
        response = self.client.post(reverse('login'), {
            'correoUsuario': 'testuser@example.com',
            'passwordUsuario': 'wrongpass'
        })
        self.assertContains(response, 'Contraseña incorrecta')

    def test_login_view_usuario_no_existe(self):
        response = self.client.post(reverse('login'), {
            'correoUsuario': 'noexiste@example.com',
            'passwordUsuario': 'algo'
        })