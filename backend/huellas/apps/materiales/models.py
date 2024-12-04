from django.db import models

class Material(models.Model):
    nombre = models.CharField(max_length=255)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    nivel_minimo = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

class TipoPapel(models.Model):
    material = models.OneToOneField('Material', on_delete=models.CASCADE)
    gramaje = models.PositiveIntegerField()
    tipo = models.CharField(max_length=255)
    color = models.CharField(max_length=50)
    textura = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.tipo} - {self.color} - {self.gramaje}g'

class Tinta(models.Model):
    material = models.OneToOneField('Material', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.color} - {self.tipo}'

class Acabado(models.Model):
    material = models.OneToOneField('Material', on_delete=models.CASCADE)
    tipo_acabado = models.CharField(max_length=255)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.tipo_acabado
