from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView 
from django.urls import reverse_lazy
from .models import Cotizacion, DetalleCotizacion
from apps.notificaciones.models import TareaProduccion

class CotizacionCreateView(CreateView):
    model = Cotizacion
    fields = ['cliente', 'estado', 'margen_ganancia', 'observaciones']
    template_name = 'cotizaciones/formulario.html'
    success_url = reverse_lazy('cotizaciones')

    def form_valid(self, form):
        # Guardar la cotización
        cotizacion = form.save()

        productos = [
            {"producto_id": 1, "cantidad": 10, "precio_unitario": 100},
            {"producto_id": 2, "cantidad": 5, "precio_unitario": 50},
        ]

        # Crear detalles de cotización (ejemplo estático; en producción se puede generar dinámicamente)
        detalles = [
            DetalleCotizacion(
                cotizacion=cotizacion,
                producto_id=producto["producto_id"],
                cantidad=producto["cantidad"],
                precio_unitario=producto["precio_unitario"]
            )
            for producto in productos
        ]
        DetalleCotizacion.objects.bulk_create(detalles)

        # Calcular el total de la cotización
        cotizacion.calcular_total()

        # Asignar tareas a áreas de producción
        tareas = [
            TareaProduccion(cotizacion=cotizacion, area='Impresión', descripcion='Imprimir los productos solicitados.'),
            TareaProduccion(cotizacion=cotizacion, area='Acabado', descripcion='Aplicar el acabado final.'),
        ]
        TareaProduccion.objects.bulk_create(tareas)

        return super().form_valid(form)



class CotizacionListView(ListView):
    model = Cotizacion
    template_name = 'cotizaciones/lista.html'
    context_object_name = 'cotizaciones'

class CotizacionDetailView(DetailView):
    model = Cotizacion
    template_name = 'cotizaciones/detalle.html'
    context_object_name = 'cotizacion'

class CotizacionCreateView(CreateView):
    model = Cotizacion
    fields = ['cliente', 'estado', 'total', 'margen_ganancia', 'observaciones']
    template_name = 'cotizaciones/formulario.html'
    success_url = reverse_lazy('cotizaciones')

class CotizacionUpdateView(UpdateView):
    model = Cotizacion
    fields = ['cliente', 'estado', 'total', 'margen_ganancia', 'observaciones']
    template_name = 'cotizaciones/formulario.html'
    success_url = reverse_lazy('cotizaciones')

class CotizacionDeleteView(DeleteView):
    model = Cotizacion
    template_name = 'cotizaciones/confirmar_eliminacion.html'
    success_url = reverse_lazy('cotizaciones')
