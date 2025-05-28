# apps/cuentas/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefono', 'cargo', 'departamento', 'avatar', 'fecha_nacimiento', 'biografia']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Este email ya está en uso.')
        return email