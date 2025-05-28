from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    detalle_facturacion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)  # Agregar este campo
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
        
    class Meta:
        db_table = 'cliente'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
