from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255)
    tipo_encuadernacion = models.CharField(max_length=255)
    imagen = models.URLField(null=True, blank=True)
    plantilla = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nombre
