from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Cotizacion, DetalleCotizacion

class CotizacionCreateView(CreateView):
    model = Cotizacion
    fields = fields = '__all__'
    template_name = 'cotizaciones/formulario.html'
    success_url = reverse_lazy('cotizacion_list')

    def form_valid(self, form):
        cotizacion = form.save(commit=False)
        cotizacion.sub_total = cotizacion.total / (1 + cotizacion.margen_ganancia / 100)
        cotizacion.save()
        return super().form_valid(form)

class CotizacionListView(ListView):
    model = Cotizacion
    template_name = 'cotizaciones/lista.html'
    context_object_name = 'cotizaciones'

class CotizacionDetailView(DetailView):
    model = Cotizacion
    template_name = 'cotizaciones/detalle.html'
    context_object_name = 'cotizacion'

class CotizacionUpdateView(UpdateView):
    model = Cotizacion
    fields = '__all__'
    template_name = 'cotizaciones/formulario.html'
    success_url = reverse_lazy('cotizacion_list')

    def form_valid(self, form):
        cotizacion = form.save(commit=False)
        cotizacion.sub_total = cotizacion.total / (1 + cotizacion.margen_ganancia / 100)
        cotizacion.save()
        return super().form_valid(form)

class CotizacionDeleteView(DeleteView):
    model = Cotizacion
    template_name = 'cotizaciones/confirmar_eliminacion.html'
    success_url = reverse_lazy('cotizacion_list')
