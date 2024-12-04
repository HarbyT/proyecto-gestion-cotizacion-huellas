from django.views.generic import ListView
from .models import TareaProduccion

class TareaProduccionListView(ListView):
    model = TareaProduccion
    template_name = 'tareas/lista.html'
    context_object_name = 'tareas'

