from django.db import models
from Aplicaciones.UsuarioSensor.models import UsuarioSensor

class ConsumoHistorico(models.Model):
    consumoTotal = models.FloatField()
    maxConsumo = models.FloatField()
    minConsumo = models.FloatField()
    fechaPeriodo = models.DateField()
    usuarioSensor = models.ForeignKey(UsuarioSensor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuarioSensor} - {self.fechaPeriodo} - Total: {self.consumoTotal} L"

