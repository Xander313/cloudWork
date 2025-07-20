from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import TipoMensaje

class TipoMensajeModelTest(TestCase):
    def setUp(self):
        self.tipo_mensaje = TipoMensaje.objects.create(
            tipoAlerta="Alerta Test",
            mensaje_default="Este es un mensaje de prueba"
        )
    
    def test_tipo_mensaje_creation(self):
        """Test que verifica la creación correcta de un TipoMensaje"""
        self.assertEqual(self.tipo_mensaje.tipoAlerta, "Alerta Test")
        self.assertEqual(self.tipo_mensaje.mensaje_default, "Este es un mensaje de prueba")
    
    def test_tipo_mensaje_str_representation(self):
        """Test que verifica el método __str__ del modelo"""
        self.assertEqual(str(self.tipo_mensaje), "Alerta Test")

class TipoMensajeViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tipo_mensaje = TipoMensaje.objects.create(
            tipoAlerta="Alerta Inicial",
            mensaje_default="Mensaje inicial"
        )
        self.agregar_url = reverse('agregar_tipo_mensaje')
        self.lista_url = reverse('lista_tipo_mensaje')
    
    def test_agregar_tipo_mensaje_get(self):
        """Test que verifica que la vista de agregar carga correctamente"""
        response = self.client.get(self.agregar_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/agregar_tipo_mensaje.html')
    
    def test_agregar_tipo_mensaje_post(self):
        """Test que verifica la creación de un nuevo TipoMensaje"""
        data = {
            'tipoAlerta': 'Nueva Alerta',
            'mensaje_default': 'Nuevo mensaje por defecto'
        }
        response = self.client.post(self.agregar_url, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.lista_url)
        
        self.assertTrue(TipoMensaje.objects.filter(tipoAlerta='Nueva Alerta').exists())
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Tipo de mensaje creado exitosamente!')
    
    def test_agregar_tipo_mensaje_post_invalid(self):
        """Test que verifica el manejo de errores al crear un TipoMensaje"""
        data = {}
        response = self.client.post(self.agregar_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/agregar_tipo_mensaje.html')
    
    def test_editar_tipo_mensaje_get(self):
        """Test que verifica que la vista de editar carga correctamente"""
        url = reverse('editar_tipo_mensaje', args=[self.tipo_mensaje.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/editar_tipo_mensaje.html')
        self.assertEqual(response.context['tipo'], self.tipo_mensaje)
    
    def test_editar_tipo_mensaje_post(self):
        """Test que verifica la actualización de un TipoMensaje"""
        url = reverse('editar_tipo_mensaje', args=[self.tipo_mensaje.id])
        data = {
            'tipoAlerta': 'Alerta Actualizada',
            'mensaje_default': 'Mensaje actualizado'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.lista_url)
        
        updated = TipoMensaje.objects.get(id=self.tipo_mensaje.id)
        self.assertEqual(updated.tipoAlerta, 'Alerta Actualizada')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Tipo de mensaje actualizado correctamente.')
    
    def test_editar_tipo_mensaje_post_invalid(self):
        """Test que verifica el manejo de errores al editar un TipoMensaje"""
        url = reverse('editar_tipo_mensaje', args=[self.tipo_mensaje.id])
        data = {}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/editar_tipo_mensaje.html')
    
    def test_eliminar_tipo_mensaje(self):
        """Test que verifica la eliminación de un TipoMensaje"""
        tipo_a_eliminar = TipoMensaje.objects.create(
            tipoAlerta="Alerta a eliminar",
            mensaje_default="Este será eliminado"
        )
        
        url = reverse('eliminar_tipo_mensaje', args=[tipo_a_eliminar.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.lista_url)
        
        with self.assertRaises(TipoMensaje.DoesNotExist):
            TipoMensaje.objects.get(id=tipo_a_eliminar.id)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Tipo de mensaje eliminado correctamente.')
        
    def test_eliminar_tipo_mensaje_invalid_id(self):
        """Test que verifica el manejo de IDs inválidos al eliminar"""
        url = reverse('eliminar_tipo_mensaje', args=[999])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lista_tipo_mensaje'))
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('no existe' in str(msg) for msg in messages))