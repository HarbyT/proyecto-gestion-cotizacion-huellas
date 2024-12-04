from django.urls import path
from .views import ProductoListView, ProductoDetailView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView

urlpatterns = [
    path('', ProductoListView.as_view(), name='productos'),
    path('<int:pk>/', ProductoDetailView.as_view(), name='producto_detalle'),
    path('crear/', ProductoCreateView.as_view(), name='producto_crear'),
    path('<int:pk>/editar/', ProductoUpdateView.as_view(), name='producto_editar'),
    path('<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='producto_eliminar'),
]
