from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin  # <-- Importa el mixin
from .models import Producto

# Lista de productos
class ProductoListView(LoginRequiredMixin, ListView):  # <-- Agrega el mixin
    model = Producto
    template_name = 'productos/lista.html'
    context_object_name = 'productos'

# Detalle de un producto
class ProductoDetailView(LoginRequiredMixin, DetailView):  # <-- Agrega el mixin
    model = Producto
    template_name = 'productos/detalle.html'
    context_object_name = 'producto'

# Crear un producto
class ProductoCreateView(LoginRequiredMixin, CreateView):  # <-- Agrega el mixin
    model = Producto
    fields = ['nombre', 'categoria', 'tipo_encuadernacion', 'imagen', 'plantilla']
    template_name = 'productos/formulario.html'
    success_url = reverse_lazy('producto_list')

# Editar un producto
class ProductoUpdateView(LoginRequiredMixin, UpdateView):  # <-- Agrega el mixin
    model = Producto
    fields = ['nombre', 'categoria', 'tipo_encuadernacion', 'imagen', 'plantilla']
    template_name = 'productos/formulario.html'
    success_url = reverse_lazy('producto_list')

# Eliminar un producto
class ProductoDeleteView(LoginRequiredMixin, DeleteView):  # <-- Agrega el mixin
    model = Producto
    template_name = 'productos/confirmar_eliminacion.html'
    success_url = reverse_lazy('producto_list')
