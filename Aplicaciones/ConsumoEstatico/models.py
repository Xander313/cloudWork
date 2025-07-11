from django.db import models
from Aplicaciones.UsuarioSensor.models import UsuarioSensor

class ConsumoEstatico(models.Model):
    consumoEstatico = models.FloatField()
    fechaCorte = models.DateTimeField(auto_now_add=True)
    usuarioSensor = models.ForeignKey(UsuarioSensor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuarioSensor} - {self.consumoEstatico} L - {self.fechaCorte.date()}"
