from django.test import TestCase
from django.urls import reverse
from .models import Sensor

class SensorTests(TestCase):
    def setUp(self):
        self.admin_session = self.client.session
        self.admin_session['es_admin'] = True
        self.admin_session.save()

        self.sensor = Sensor.objects.create(
            sensorID=1,
            nombreSensor='Sensor Uno',
            latitud=-0.737,
            longitud=-78.641,
        )

    def test_lista_sensor_admin(self):
        # Admin ve la lista
        response = self.client.get(reverse('lista_sensor'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sensor Uno')

    def test_lista_sensor_no_admin(self):
        # Sin admin, redirige a login
        self.client.session.flush()
        response = self.client.get(reverse('lista_sensor'))
        self.assertRedirects(response, reverse('login'))

    def test_agregar_sensor_valido(self):
        response = self.client.post(reverse('agregar_sensor'), {
            'sensorID': 2,  # id NO duplicado
            'nombreSensor': 'Sensor Dos',
            'latitud': '-0.7375',
            'longitud': '-78.6415',
        })

        # El view debería redirigir a la lista de sensores tras agregar con éxito
        self.assertRedirects(response, reverse('lista_sensor'))

        # Comprobar que el sensor se creó en la BD
        self.assertTrue(Sensor.objects.filter(sensorID=2).exists())



