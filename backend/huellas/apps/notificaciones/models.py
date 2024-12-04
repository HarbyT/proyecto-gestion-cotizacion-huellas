from django.db import models
from apps.cotizaciones.models import Cotizacion
from apps.productos.models import Producto


class TareaProduccion(models.Model):
    cotizacion = models.ForeignKey('cotizaciones.Cotizacion', on_delete=models.CASCADE, related_name='tareas')
    area = models.CharField(max_length=255, choices=[('Impresión', 'Impresión'), ('Acabado', 'Acabado'), ('Empaque', 'Empaque')])
    descripcion = models.TextField()
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f'Tarea para {self.area} - Cotización #{self.cotizacion.id}'

class Notificacion(models.Model):
    cotizacion = models.ForeignKey('cotizaciones.Cotizacion', on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notificación para Cotización #{self.cotizacion.id}'
    