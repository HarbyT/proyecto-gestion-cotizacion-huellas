from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cliente
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class ClienteList(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10
    
    def get_queryset(self):
        return Cliente.objects.filter(activo=True).order_by('-fecha_creacion')

class ClienteDetail(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente'

class ClienteCreate(LoginRequiredMixin, CreateView):
    model = Cliente
    template_name = 'clientes/cliente_form.html'
    fields = ['nombre', 'correo', 'telefono', 'direccion', 'detalle_facturacion', 'activo']
    success_url = reverse_lazy('clientes:cliente_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Cliente "{form.instance.nombre}" creado exitosamente.')
        return super().form_valid(form)

class ClienteUpdate(LoginRequiredMixin, UpdateView):
    model = Cliente
    template_name = 'clientes/cliente_form.html'
    fields = ['nombre', 'correo', 'telefono', 'direccion', 'detalle_facturacion', 'activo']
    success_url = reverse_lazy('clientes:cliente_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Cliente "{form.instance.nombre}" actualizado exitosamente.')
        return super().form_valid(form)

class ClienteDelete(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes:cliente_list')
    
    def delete(self, request, *args, **kwargs):
        cliente = self.get_object()
        messages.success(request, f'Cliente "{cliente.nombre}" eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

@require_POST
def enviar_contacto(request):
    nombre = request.POST.get('nombre')
    email = request.POST.get('email')
    telefono = request.POST.get('telefono')
    mensaje = request.POST.get('mensaje')

    send_mail(
        subject=f'Nuevo contacto de {nombre}',
        message=f'Nombre: {nombre}\nEmail: {email}\nTeléfono: {telefono}\n\nMensaje:\n{mensaje}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.CONTACT_EMAIL],
    )
    messages.success(request, "¡Gracias por contactarnos! Tu mensaje fue enviado y nos pondremos en contacto contigo pronto.")
    return redirect('home')
