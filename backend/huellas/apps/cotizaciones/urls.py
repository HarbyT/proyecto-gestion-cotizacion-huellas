from django.urls import path
from . import views

app_name = 'cotizaciones'

urlpatterns = [
    # Lista y CRUD básico
    path('', views.CotizacionListView.as_view(), name='cotizacion_list'),
    path('crear/', views.CotizacionCreateView.as_view(), name='cotizacion_create'),
    path('<int:pk>/', views.CotizacionDetailView.as_view(), name='cotizacion_detail'),
    path('<int:pk>/editar/', views.CotizacionUpdateView.as_view(), name='cotizacion_update'),
    path('<int:pk>/eliminar/', views.CotizacionDeleteView.as_view(), name='cotizacion_delete'),
    
    # Reportes básicos
    path('reportes/', views.ReportesCotizacionView.as_view(), name='reportes'),
]
