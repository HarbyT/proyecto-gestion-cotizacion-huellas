from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Perfil
from .forms import PerfilForm, UsuarioForm

@login_required
def perfil(request):
    perfil = None
    if hasattr(request.user, 'perfil'):
        perfil = request.user.perfil
    return render(request, 'cuentas/perfil.html', {'perfil': perfil})

class PerfilDetailView(LoginRequiredMixin, DetailView):
    """Vista para mostrar perfil del usuario actual"""
    model = Perfil
    template_name = 'cuentas/perfil_detalle.html'
    context_object_name = 'perfil'
    
    def get_object(self):
        # Siempre retorna el perfil del usuario logueado
        perfil, created = Perfil.objects.get_or_create(user=self.request.user)
        return perfil
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cotizaciones_recientes'] = self.request.user.cotizaciones_creadas.all()[:5]
        return context

class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para editar perfil del usuario actual"""
    model = Perfil
    form_class = PerfilForm
    template_name = 'cuentas/perfil_editar.html'
    success_url = reverse_lazy('cuentas:perfil')
    
    def get_object(self):
        perfil, created = Perfil.objects.get_or_create(user=self.request.user)
        return perfil
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado exitosamente.')
        return super().form_valid(form)

class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para editar datos básicos del usuario"""
    model = User
    form_class = UsuarioForm
    template_name = 'cuentas/usuario_editar.html'
    success_url = reverse_lazy('cuentas:perfil')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Datos de usuario actualizados exitosamente.')
        return super().form_valid(form)