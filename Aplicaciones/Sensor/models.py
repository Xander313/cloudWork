from django.db import models

# Create your models here.
class Sensor(models.Model):
    sensorID = models.IntegerField(primary_key=True)
    nombreSensor = models.CharField(max_length=100)
    fechaInscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombreSensor