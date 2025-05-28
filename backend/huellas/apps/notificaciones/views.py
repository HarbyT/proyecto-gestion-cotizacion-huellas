from django.views.generic import ListView
from .models import TareaProduccion
from django.shortcuts import render
from django.http import HttpResponse

class TareaProduccionListView(ListView):
    model = TareaProduccion
    template_name = 'tareas/lista.html'
    context_object_name = 'tareas'

def notificacion_list(request):
    return HttpResponse("Lista de notificaciones - En desarrollo")

def marcar_leida(request, pk):
    return HttpResponse(f"Marcar notificación {pk} como leída - En desarrollo")

def marcar_todas_leidas(request):
    return HttpResponse("Marcar todas las notificaciones como leídas - En desarrollo")

