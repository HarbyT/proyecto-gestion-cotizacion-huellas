from django.urls import path
from .views import (
    ProductoListView, ProductoDetailView, ProductoCreateView, 
    ProductoUpdateView, ProductoDeleteView, CatalogoPublicoView,
    CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView
)
from . import views

app_name = 'productos'

urlpatterns = [
    # URLs principales de productos
    path('', ProductoListView.as_view(), name='producto_list'),
    path('nuevo/', ProductoCreateView.as_view(), name='producto_create'),
    path('<int:pk>/', ProductoDetailView.as_view(), name='producto_detail'),
    path('<int:pk>/editar/', ProductoUpdateView.as_view(), name='producto_update'),
    path('<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='producto_delete'),
    
    # Catálogo público
    path('catalogo/', CatalogoPublicoView.as_view(), name='catalogo_publico'),
    
    # URLs de categorías
    path('categorias/', CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/nueva/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/editar/', CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', CategoriaDeleteView.as_view(), name='categoria_delete'),
    
    # AJAX endpoints para búsqueda desde cotizaciones
    path('ajax/buscar/', views.buscar_productos_ajax, name='buscar_productos_ajax'),
    path('ajax/<int:producto_id>/', views.obtener_producto_ajax, name='obtener_producto_ajax'),
    path('ajax/lista/', views.ProductoListAjaxView.as_view(), name='producto_list_ajax'),

    # URLs adicionales
    path('categoria/<int:categoria_id>/', ProductoListView.as_view(), name='productos_por_categoria'),
    path('buscar/', ProductoListView.as_view(), name='buscar_productos'),
]
