from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from .models import Producto, Categoria
from .forms import ProductoForm, ProductoFilterForm, CategoriaForm
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Producto

# Lista de productos con filtros y búsqueda
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/lista.html'
    context_object_name = 'productos'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Producto.objects.select_related('categoria').all()
        
        # Filtro por categoría desde URL
        categoria_id = self.kwargs.get('categoria_id')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        
        # Filtro por búsqueda
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) | 
                Q(descripcion__icontains=search) |
                Q(categoria__nombre__icontains=search)
            )
        
        # Filtro por categoría desde GET
        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
            
        # Filtro por tipo de papel
        tipo_papel = self.request.GET.get('tipo_papel')
        if tipo_papel:
            queryset = queryset.filter(tipo_papel=tipo_papel)
            
        # Filtro por estado activo
        activo = self.request.GET.get('activo')
        if activo == 'true':
            queryset = queryset.filter(activo=True)
        elif activo == 'false':
            queryset = queryset.filter(activo=False)
            
        # Filtro por rango de gramaje
        gramaje_min = self.request.GET.get('gramaje_min')
        gramaje_max = self.request.GET.get('gramaje_max')
        if gramaje_min:
            queryset = queryset.filter(gramaje__gte=gramaje_min)
        if gramaje_max:
            queryset = queryset.filter(gramaje__lte=gramaje_max)
            
        return queryset.order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.filter(activa=True)
        context['form'] = ProductoFilterForm(self.request.GET)
        context['search_query'] = self.request.GET.get('search', '')
        
        # Agregar información de filtros activos
        context['filtros_activos'] = {
            'search': self.request.GET.get('search'),
            'categoria': self.request.GET.get('categoria'),
            'tipo_papel': self.request.GET.get('tipo_papel'),
            'activo': self.request.GET.get('activo'),
        }
        
        return context

# Detalle de producto con todas sus especificaciones
class ProductoDetailView(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = 'productos/detalle.html'
    context_object_name = 'producto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Productos relacionados de la misma categoría
        context['productos_relacionados'] = Producto.objects.filter(
            categoria=self.object.categoria,
            activo=True
        ).exclude(id=self.object.id)[:4]
        return context

# Crear producto con formulario completo
class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/formulario.html'
    success_url = reverse_lazy('productos:producto_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Producto "{form.instance.nombre}" creado exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirigir al detalle del producto creado
        return reverse_lazy('productos:producto_detail', kwargs={'pk': self.object.pk})

# Editar producto
class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/formulario.html'
    
    def get_success_url(self):
        return reverse_lazy('productos:producto_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, f'Producto "{form.instance.nombre}" actualizado exitosamente.')
        return super().form_valid(form)

# Eliminar producto
class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productos/confirmar_eliminacion.html'
    success_url = reverse_lazy('productos:producto_list')
    context_object_name = 'producto'
    
    def delete(self, request, *args, **kwargs):
        producto = self.get_object()
        messages.success(request, f'Producto "{producto.nombre}" eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

# Vista para catálogo público (sin login requerido)
class CatalogoPublicoView(ListView):
    model = Producto
    template_name = 'productos/catalogo_publico.html'
    context_object_name = 'productos'
    paginate_by = 16
    
    def get_queryset(self):
        queryset = Producto.objects.filter(activo=True).select_related('categoria')
        
        # Filtros públicos
        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
            
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) | 
                Q(descripcion__icontains=search)
            )
            
        return queryset.order_by('categoria__nombre', 'nombre')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.filter(activa=True)
        context['es_catalogo_publico'] = True
        return context

# === VISTAS PARA CATEGORÍAS ===

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'productos/categoria_lista.html'
    context_object_name = 'categorias'
    paginate_by = 10
    
    def get_queryset(self):
        return Categoria.objects.all().order_by('nombre')

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'productos/categoria_formulario.html'
    success_url = reverse_lazy('productos:categoria_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Categoría "{form.instance.nombre}" creada exitosamente.')
        return super().form_valid(form)

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'productos/categoria_formulario.html'
    success_url = reverse_lazy('productos:categoria_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Categoría "{form.instance.nombre}" actualizada exitosamente.')
        return super().form_valid(form)

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'productos/categoria_confirmar_eliminacion.html'
    success_url = reverse_lazy('productos:categoria_list')
    context_object_name = 'categoria'
    
    def delete(self, request, *args, **kwargs):
        categoria = self.get_object()
        # Verificar si tiene productos asociados
        if categoria.producto_set.exists():
            messages.error(request, f'No se puede eliminar la categoría "{categoria.nombre}" porque tiene productos asociados.')
            return redirect('productos:categoria_list')
        
        messages.success(request, f'Categoría "{categoria.nombre}" eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

class ProductoListAjaxView(View):
    """Vista AJAX para obtener lista de productos"""
    
    def get(self, request):
        try:
            productos = Producto.objects.filter(activo=True).select_related('categoria').values(
                'id', 'nombre', 'descripcion', 'precio_base', 
                'tipo_papel', 'gramaje', 'tamaño', 'acabados_especiales',
                'categoria__nombre'
            )
            return JsonResponse(list(productos), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def buscar_productos_ajax(request):
    """Vista AJAX para buscar productos"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) | 
            Q(descripcion__icontains=query),
            activo=True
        ).select_related('categoria').values(
            'id', 'nombre', 'descripcion', 'precio_base',
            'tipo_papel', 'gramaje', 'tamaño', 'acabados_especiales',
            'categoria__nombre'
        )[:10]
        
        return JsonResponse(list(productos), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def obtener_producto_ajax(request, producto_id):
    """Vista AJAX para obtener detalles de un producto"""
    try:
        producto = get_object_or_404(Producto, pk=producto_id, activo=True)
        data = {
            'id': producto.id,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio_base': float(producto.precio_base) if producto.precio_base else 0,
            'tipo_papel': producto.tipo_papel,
            'gramaje': producto.gramaje,
            'tamaño': producto.tamaño,
            'acabados_especiales': producto.acabados_especiales,
            'categoria': producto.categoria.nombre if producto.categoria else None,
        }
        return JsonResponse(data)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
