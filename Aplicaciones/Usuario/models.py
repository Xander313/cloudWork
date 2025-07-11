from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombreUsuario = models.CharField(max_length=100)
    correoUsuario = models.EmailField(max_length=100, unique=True)
    passwordUsuario = models.CharField(max_length=100)
    fechaCreacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombreUsuario