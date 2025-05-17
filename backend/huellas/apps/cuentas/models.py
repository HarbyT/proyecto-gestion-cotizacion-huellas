# filepath: backend/huellas/cuentas/models.py
from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    # otros campos

    def __str__(self):
        return self.user.username
