from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date
from apps.clientes.models import Cliente
from apps.productos.models import Producto

# Función nombrada para reemplazar la lambda
def fecha_vencimiento_default():
    return timezone.now().date() + timedelta(days=30)

class Cotizacion(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('enviada', 'Enviada'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
        ('vencida', 'Vencida'),
    ]
    
    # Información básica
    codigo = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Código",
        default="COT-TEMP-0001"  # Default simple para migración
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    # Fecha de vencimiento con función nombrada en lugar de lambda
    fecha_vencimiento = models.DateField(
        default=fecha_vencimiento_default,
        verbose_name="Fecha de vencimiento"
    )
    
    estado = models.CharField(
        max_length=20, 
        choices=ESTADOS, 
        default='borrador',
        verbose_name="Estado"
    )
    
    # Información del negocio
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    condiciones_pago = models.TextField(blank=True, verbose_name="Condiciones de pago")
    tiempo_entrega = models.CharField(max_length=100, blank=True, verbose_name="Tiempo de entrega")
    
    # Cálculos financieros
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Subtotal")
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Descuento (%)")
    descuento_valor = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Descuento ($)")
    
    # IVA
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=19, verbose_name="IVA (%)")
    iva_valor = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="IVA ($)")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total")
    
    # Metadatos
    usuario_creador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Creado por",
        default=1  # Default simple para migración
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        db_table = 'cotizacion'
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.codigo} - {self.cliente.nombre}"

class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='detalles', verbose_name="Cotización")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    
    # Información del producto en el momento de la cotización
    nombre_producto = models.CharField(max_length=200, verbose_name="Nombre del producto")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    
    # Especificaciones técnicas - AGREGAR DEFAULTS
    cantidad = models.IntegerField(default=1, verbose_name="Cantidad")
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Costo unitario")
    margen_utilidad = models.DecimalField(max_digits=5, decimal_places=2, default=30, verbose_name="Margen de utilidad (%)")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio unitario")
    
    # Descuentos específicos del item
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Descuento (%)")
    descuento_valor = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Descuento ($)")
    
    # IVA específico del item
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=19, verbose_name="IVA (%)")
    iva_valor = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="IVA ($)")
    
    # Total del detalle
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Subtotal")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total")
    
    # Especificaciones adicionales
    especificaciones_tecnicas = models.TextField(blank=True, verbose_name="Especificaciones técnicas")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    class Meta:
        db_table = 'detalle_cotizacion'
        verbose_name = "Detalle de cotización"
        verbose_name_plural = "Detalles de cotización"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.cotizacion.codigo} - {self.nombre_producto}"
