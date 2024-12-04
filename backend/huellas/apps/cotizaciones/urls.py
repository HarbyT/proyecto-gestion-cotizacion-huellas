from django.urls import path
from .views import (
    CotizacionListView,
    CotizacionDetailView,
    CotizacionCreateView,
    CotizacionUpdateView,
    CotizacionDeleteView
)

urlpatterns = [
    path('', CotizacionListView.as_view(), name='cotizaciones'),
    path('<int:pk>/', CotizacionDetailView.as_view(), name='cotizacion_detalle'),
    path('crear/', CotizacionCreateView.as_view(), name='cotizacion_crear'),
    path('<int:pk>/editar/', CotizacionUpdateView.as_view(), name='cotizacion_editar'),
    path('<int:pk>/eliminar/', CotizacionDeleteView.as_view(), name='cotizacion_eliminar'),
]
