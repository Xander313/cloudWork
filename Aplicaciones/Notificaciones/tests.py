from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Sensor.models import Sensor
from Aplicaciones.UsuarioSensor.models import UsuarioSensor
from Aplicaciones.TipoMensaje.models import TipoMensaje
from Aplicaciones.Notificaciones.models import Notificacion
from Aplicaciones.ConsumoHistorico.models import ConsumoHistorico
from Aplicaciones.consumoDinamico.models import ConsumoDinamico
from Aplicaciones.ConsumoEstatico.models import ConsumoEstatico
from Aplicaciones.LimiteUsuario.models import LimiteUsuario

class NotificacionesViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(nombre="Test User")
        self.sensor = Sensor.objects.create(
            sensorID=1,
            nombreSensor="Sensor 1",
            latitud="-0.75",
            longitud="-78.6"
        )
        self.usuario_sensor = UsuarioSensor.objects.create(
            usuario=self.usuario,
            sensor=self.sensor,
            ubicacionSensor="Casa"
        )
        self.tipo_mensaje = TipoMensaje.objects.create(tipoAlerta="Consumo")

        self.notificacion = Notificacion.objects.create(
            mensaje="Mensaje de prueba",
            usuarioSensor=self.usuario_sensor,
            tipoMensaje=self.tipo_mensaje
        )

    def test_obtener_notificaciones_sensor_texto(self):
        url = reverse('obtener_notificaciones_sensor_texto', args=[self.usuario_sensor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('mensaje', response.json()['notificaciones'][0])

    def test_obtener_notificaciones_sensor_json(self):
        ConsumoDinamico.objects.create(
            consumoDinamico=120.5,
            fechaCorte=now(),
            usuarioSensor=self.usuario_sensor
        )
        ConsumoEstatico.objects.create(
            consumoEstatico=3000,
            usuarioSensor=self.usuario_sensor
        )
        LimiteUsuario.objects.create(
            limiteDiario=1500,
            umbralAlerta=10000,
            tiempoMinutos=60,
            usuarioSensor=self.usuario_sensor
        )

        url = reverse('obtener_notificaciones_sensor', args=[self.usuario_sensor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('grafico', response.json())

    def test_ver_notificaciones_por_usuario(self):
        session = self.client.session
        session['usuario_id'] = self.usuario.id
        session.save()

        url = reverse('ver_notificaciones_por_usuario', args=[self.usuario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ubicacionSensor')

    def test_eliminar_notificacion(self):
        url = reverse('eliminar_notificacion', args=[self.notificacion.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('lista_notificaciones'))
        self.assertFalse(Notificacion.objects.filter(id=self.notificacion.id).exists())

    def test_editar_notificacion_get(self):
        url = reverse('editar_notificacion', args=[self.notificacion.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.notificacion.mensaje)

    def test_editar_notificacion_post(self):
        url = reverse('editar_notificacion', args=[self.notificacion.id])
        response = self.client.post(url, {
            'mensaje': 'Nuevo mensaje',
            'estado': True
        })
        self.assertRedirects(response, reverse('lista_notificaciones'))
        self.notificacion.refresh_from_db()
        self.assertEqual(self.notificacion.mensaje, 'Nuevo mensaje')

    def test_consumo_dinamico_hoy(self):
        ConsumoDinamico.objects.create(
            consumoDinamico=50,
            fechaCorte=now(),
            usuarioSensor=self.usuario_sensor
        )
        url = reverse('consumo-dinamico-hoy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_reporte_consumo_json(self):
        ConsumoHistorico.objects.create(
            usuarioSensor=self.usuario_sensor,
            fechaPeriodo=now().date(),
            consumoTotal=500,
            maxConsumo=300,
            minConsumo=100
        )
        url = reverse('reporte_consumo_json', args=[self.usuario_sensor.id])
        response = self.client.get(url)
        self.assertIn("consumo_total", response.json())

    def test_reporte_consumo_pie(self):
        ConsumoHistorico.objects.create(
            usuarioSensor=self.usuario_sensor,
            fechaPeriodo=now().date(),
            consumoTotal=500,
            maxConsumo=300,
            minConsumo=100
        )
        url = reverse('reporte_consumo_pie', args=[self.usuario_sensor.id])
        response = self.client.get(url)
        self.assertIn("dias", response.json())

    def test_estadisticas_geograficas_json(self):
        fecha_actual = now().date()
        ConsumoHistorico.objects.create(
            usuarioSensor=self.usuario_sensor,
            fechaPeriodo=fecha_actual,
            consumoTotal=300,
            maxConsumo=200,
            minConsumo=100
        )
        url = reverse('estadisticas_geograficas')
        response = self.client.get(url, {'inicio': fecha_actual.isoformat(), 'fin': fecha_actual.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_estadistica_presentacion_render(self):
        url = reverse('estadisticaPresenracion', args=[self.usuario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'sensor')

    def test_admin_estadisticas_render(self):
        response = self.client.get(reverse('admin-estadisticas-geograficas'))
        self.assertEqual(response.status_code, 200)

    def test_admin_estadisticas_avanzadas_render(self):
        response = self.client.get(reverse('admin-estadisticas-geograficas-avanzadas'))
        self.assertEqual(response.status_code, 200)
