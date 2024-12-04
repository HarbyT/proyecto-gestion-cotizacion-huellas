from django.db import models
from django.contrib.auth.models import User
from apps.clientes.models import Cliente
from apps.productos.models import Producto

class Cotizacion(models.Model):
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)
    fecha_creacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('completada', 'Completada')])
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)  # IVA predeterminado al 19%
    margen_ganancia = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    observaciones = models.TextField(null=True, blank=True)

    def calcular_total(self):
        subtotal = sum(detalle.sub_total for detalle in self.detalles.all())
        iva_calculado = subtotal * (self.iva / 100)
        self.total = subtotal + iva_calculado
        self.save()

    def __str__(self):
        return f'Cotización #{self.id} - {self.cliente.nombre}'


class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey('Cotizacion', on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        # Calcula el subtotal automáticamente
        self.sub_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} en Cotización #{self.cotizacion.id}'

