from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Producto

# Lista de productos
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/lista.html'
    context_object_name = 'productos'

# Detalle de un producto
class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/detalle.html'
    context_object_name = 'producto'

# Crear un producto
class ProductoCreateView(CreateView):
    model = Producto
    fields = ['nombre', 'categoria', 'tipo_encuadernacion', 'imagen', 'plantilla']
    template_name = 'productos/formulario.html'
    success_url = reverse_lazy('producto_list')

# Editar un producto
class ProductoUpdateView(UpdateView):
    model = Producto
    fields = ['nombre', 'categoria', 'tipo_encuadernacion', 'imagen', 'plantilla']
    template_name = 'productos/formulario.html'
    success_url = reverse_lazy('producto_list')

# Eliminar un producto
class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/confirmar_eliminacion.html'
    success_url = reverse_lazy('producto_list')
