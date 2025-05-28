# filepath: backend/huellas/cuentas/models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True)
    cargo = models.CharField(max_length=100, blank=True)
    departamento = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    biografia = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"
    
    @property
    def nombre_completo(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()

# Signal para crear perfil automáticamente
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
