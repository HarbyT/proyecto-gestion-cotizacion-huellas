from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(unique=True)
    detalle_facturacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre
