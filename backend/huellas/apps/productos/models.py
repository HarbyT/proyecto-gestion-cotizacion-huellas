from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    # Opciones para campos de selección
    TIPOS_PAPEL = [
        ('bond', 'Bond'),
        ('propalcote', 'Propalcote'),
        ('opalina', 'Opalina'),
        ('couche', 'Couché'),
        ('kraft', 'Kraft'),
        ('cartulina', 'Cartulina'),
        ('adhesivo', 'Adhesivo'),
        ('sintetico', 'Sintético'),
        ('otro', 'Otro'),
    ]
    
    TIPOS_ENCUADERNACION = [
        ('grapado', 'Grapado'),
        ('espiral', 'Espiral'),
        ('anillado', 'Anillado'),
        ('cosido', 'Cosido'),
        ('pegado', 'Pegado'),
        ('tapa_dura', 'Tapa Dura'),
        ('tapa_blanda', 'Tapa Blanda'),
        ('sin_encuadernacion', 'Sin Encuadernación'),
    ]
    
    ACABADOS = [
        ('barniz_uv', 'Barniz UV'),
        ('laminado_mate', 'Laminado Mate'),
        ('laminado_brillante', 'Laminado Brillante'),
        ('relieve', 'Relieve'),
        ('hot_stamping', 'Hot Stamping'),
        ('troquelado', 'Troquelado'),
        ('perforado', 'Perforado'),
        ('ninguno', 'Ninguno'),
    ]
    
    # Información básica
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    subcategoria = models.CharField(max_length=100, blank=True)
    
    # Especificaciones técnicas
    tipo_papel = models.CharField(max_length=50, choices=TIPOS_PAPEL, blank=True)
    gramaje = models.PositiveIntegerField(null=True, blank=True, help_text="Gramaje del papel (ej: 90, 120, 150)")
    tamaño = models.CharField(max_length=100, blank=True, help_text="Ej: A4, Carta, 10x15cm, Medio pliego")
    numero_paginas = models.PositiveIntegerField(null=True, blank=True)
    tipo_encuadernacion = models.CharField(max_length=50, choices=TIPOS_ENCUADERNACION, blank=True)
    acabados_especiales = models.TextField(blank=True, help_text="Describe acabados especiales o personalizados")
    
    # Imágenes y archivos
    imagen_principal = models.ImageField(upload_to='productos/imagenes/', null=True, blank=True)
    imagenes_adicionales = models.TextField(blank=True, help_text="URLs de imágenes adicionales separadas por comas")
    plantilla_ejemplo = models.FileField(upload_to='productos/plantillas/', null=True, blank=True)
    
    # Información comercial
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Campos personalizables
    atributos_adicionales = models.JSONField(default=dict, blank=True, help_text="Atributos personalizados en formato JSON")
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return f"{self.nombre} - {self.categoria}"
    
    def get_imagenes_adicionales_list(self):
        """Convierte el campo de texto de imágenes adicionales en una lista"""
        if self.imagenes_adicionales:
            return [url.strip() for url in self.imagenes_adicionales.split(',') if url.strip()]
        return []
    
    def get_acabados_display(self):
        """Retorna una representación amigable de los acabados"""
        if self.acabados_especiales:
            return self.acabados_especiales
        return "Sin acabados especiales"
