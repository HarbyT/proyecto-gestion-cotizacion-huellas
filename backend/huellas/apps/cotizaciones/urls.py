from django.urls import path
from .views import CotizacionListView, CotizacionDetailView, CotizacionCreateView, CotizacionUpdateView, CotizacionDeleteView

urlpatterns = [
    path('', CotizacionListView.as_view(), name='cotizacion_list'),
    path('<int:pk>/', CotizacionDetailView.as_view(), name='cotizacion_detail'),
    path('nuevo/', CotizacionCreateView.as_view(), name='cotizacion_create'),
    path('<int:pk>/editar/', CotizacionUpdateView.as_view(), name='cotizacion_update'),
    path('<int:pk>/eliminar/', CotizacionDeleteView.as_view(), name='cotizacion_delete'),
]
