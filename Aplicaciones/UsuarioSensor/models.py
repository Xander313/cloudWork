from django.db import models
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Sensor.models import Sensor

class UsuarioSensor(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    ubicacionSensor = models.CharField(max_length=100)
    fechaAsignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'sensor', 'ubicacionSensor')


    class Meta:
        unique_together = ('usuario', 'sensor', 'ubicacionSensor')

    
    class Meta:
        unique_together = ('usuario', 'sensor', 'ubicacionSensor')