from django.urls import path
from . import views

app_name = 'cuentas'

urlpatterns = [
    path('perfil/', views.PerfilDetailView.as_view(), name='perfil'),
    path('perfil/editar/', views.PerfilUpdateView.as_view(), name='perfil_editar'),
    path('usuario/editar/', views.UsuarioUpdateView.as_view(), name='usuario_editar'),
]