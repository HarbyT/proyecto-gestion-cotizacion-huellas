from django.db import models

class Maquina(models.Model):
    tipo = models.CharField(max_length=255)
    tamano_maximo = models.CharField(max_length=255)
    velocidad = models.CharField(max_length=255)
    costo_operacion = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.tipo
