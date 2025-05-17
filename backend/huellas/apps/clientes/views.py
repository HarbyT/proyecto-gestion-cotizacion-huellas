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
    template_name = 'cliente_list.html'
    context_object_name = 'clientes'

class ClienteDetail(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'cliente_detail.html'
    context_object_name = 'cliente'

class ClienteCreate(LoginRequiredMixin, CreateView):
    model = Cliente
    template_name = 'cliente_form.html'
    fields = '__all__'
    success_url = reverse_lazy('cliente_list')

class ClienteUpdate(LoginRequiredMixin, UpdateView):
    model = Cliente
    template_name = 'cliente_form.html'
    fields = '__all__'
    success_url = reverse_lazy('cliente_list')

class ClienteDelete(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')

@require_POST
def enviar_contacto(request):
    nombre = request.POST.get('nombre')
    email = request.POST.get('email')
    telefono = request.POST.get('telefono')
    mensaje = request.POST.get('mensaje')

    # Aquí puedes guardar en un modelo si lo deseas

    # Enviar correo
    send_mail(
        subject=f'Nuevo contacto de {nombre}',
        message=f'Nombre: {nombre}\nEmail: {email}\nTeléfono: {telefono}\n\nMensaje:\n{mensaje}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.CONTACT_EMAIL],
    )
    messages.success(request, "¡Gracias por contactarnos! Tu mensaje fue enviado y nos pondremos en contacto contigo pronto.")
    return redirect('home')
