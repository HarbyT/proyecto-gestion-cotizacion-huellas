from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

def home(request):
    return render(request, 'home.html')

def enviar_contacto(request):
    if request.method == 'POST':
        # Aquí procesarías el formulario de contacto
        messages.success(request, 'Mensaje enviado correctamente. Te contactaremos pronto.')
        return redirect('home')
    return redirect('home')