from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Cotizacion, DetalleCotizacion
from .forms import CotizacionForm, DetalleCotizacionFormSet

class CotizacionListView(LoginRequiredMixin, ListView):
    """Vista para listar cotizaciones"""
    model = Cotizacion
    template_name = 'cotizaciones/lista.html'
    context_object_name = 'cotizaciones'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Cotizacion.objects.select_related('cliente', 'usuario_creador').order_by('-fecha_creacion')
        
        # Filtros opcionales
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
            
        cliente = self.request.GET.get('cliente')
        if cliente:
            queryset = queryset.filter(cliente__nombre__icontains=cliente)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas básicas
        context['stats'] = {
            'total': Cotizacion.objects.count(),
            'borradores': Cotizacion.objects.filter(estado='borrador').count(),
            'enviadas': Cotizacion.objects.filter(estado='enviada').count(),
            'aceptadas': Cotizacion.objects.filter(estado='aceptada').count(),
        }
        
        return context

class CotizacionDetailView(LoginRequiredMixin, DetailView):
    """Vista para mostrar detalle de cotización"""
    model = Cotizacion
    template_name = 'cotizaciones/detalle.html'
    context_object_name = 'cotizacion'
    
    def get_object(self):
        return get_object_or_404(
            Cotizacion.objects.select_related('cliente', 'usuario_creador').prefetch_related('detalles__producto'),
            pk=self.kwargs['pk']
        )

class CotizacionCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear nueva cotización"""
    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'cotizaciones/formulario.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['detalles'] = DetalleCotizacionFormSet(self.request.POST, instance=self.object)
        else:
            context['detalles'] = DetalleCotizacionFormSet(instance=self.object)
            
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        detalles = context['detalles']
        
        if detalles.is_valid():
            # Asignar usuario creador
            form.instance.usuario_creador = self.request.user
            
            # Generar código automático
            if not form.instance.codigo:
                form.instance.codigo = self.generar_codigo()
            
            self.object = form.save()
            detalles.instance = self.object
            detalles.save()
            
            messages.success(self.request, f'Cotización {self.object.codigo} creada exitosamente.')
            return redirect('cotizaciones:cotizacion_detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def generar_codigo(self):
        """Generar código único para la cotización"""
        fecha = timezone.now()
        prefijo = f"COT-{fecha.year}{fecha.month:02d}"
        
        # Buscar el último número del mes
        ultima_cotizacion = Cotizacion.objects.filter(
            codigo__startswith=prefijo
        ).order_by('-codigo').first()
        
        if ultima_cotizacion:
            try:
                ultimo_numero = int(ultima_cotizacion.codigo.split('-')[-1])
                nuevo_numero = ultimo_numero + 1
            except:
                nuevo_numero = 1
        else:
            nuevo_numero = 1
            
        return f"{prefijo}-{nuevo_numero:04d}"

class CotizacionUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para editar cotización"""
    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'cotizaciones/formulario.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['detalles'] = DetalleCotizacionFormSet(self.request.POST, instance=self.object)
        else:
            context['detalles'] = DetalleCotizacionFormSet(instance=self.object)
            
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        detalles = context['detalles']
        
        if detalles.is_valid():
            self.object = form.save()
            detalles.save()
            
            messages.success(self.request, f'Cotización {self.object.codigo} actualizada exitosamente.')
            return redirect('cotizaciones:cotizacion_detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class CotizacionDeleteView(LoginRequiredMixin, DeleteView):
    """Vista para eliminar cotización"""
    model = Cotizacion
    template_name = 'cotizaciones/confirmar_eliminacion.html'
    success_url = reverse_lazy('cotizaciones:cotizacion_list')
    context_object_name = 'cotizacion'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        messages.success(request, f'Cotización {self.object.codigo} eliminada exitosamente.')
        self.object.delete()
        
        return redirect(success_url)

class ReportesCotizacionView(LoginRequiredMixin, ListView):
    """Vista para reportes de cotizaciones"""
    template_name = 'cotizaciones/reportes.html'
    
    def get_queryset(self):
        return None  # No necesitamos queryset para esta vista
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fechas por defecto (último mes)
        fecha_fin = timezone.now().date()
        fecha_inicio = fecha_fin - timedelta(days=30)
        
        # Obtener fechas de los parámetros GET si existen
        if self.request.GET.get('fecha_inicio'):
            try:
                fecha_inicio = datetime.strptime(self.request.GET.get('fecha_inicio'), '%Y-%m-%d').date()
            except:
                pass
                
        if self.request.GET.get('fecha_fin'):
            try:
                fecha_fin = datetime.strptime(self.request.GET.get('fecha_fin'), '%Y-%m-%d').date()
            except:
                pass
        
        # Filtrar cotizaciones por fechas
        cotizaciones = Cotizacion.objects.filter(
            fecha_creacion__date__range=[fecha_inicio, fecha_fin]
        )
        
        # Calcular estadísticas
        stats = {
            'total_cotizaciones': cotizaciones.count(),
            'valor_total': sum([c.total for c in cotizaciones if c.total]),
            'cotizaciones_aceptadas': cotizaciones.filter(estado='aceptada').count(),
            'borradores': cotizaciones.filter(estado='borrador').count(),
            'enviadas': cotizaciones.filter(estado='enviada').count(),
            'rechazadas': cotizaciones.filter(estado='rechazada').count(),
        }
        
        # Calcular tasa de conversión
        if stats['total_cotizaciones'] > 0:
            stats['tasa_conversion'] = round(
                (stats['cotizaciones_aceptadas'] / stats['total_cotizaciones']) * 100, 1
            )
        else:
            stats['tasa_conversion'] = 0
        
        context.update({
            'stats': stats,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
        })
        
        return context
