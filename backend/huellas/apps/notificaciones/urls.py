from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('', views.notificacion_list, name='notificacion_list'),
    path('<int:pk>/marcar-leida/', views.marcar_leida, name='marcar_leida'),
    path('marcar-todas-leidas/', views.marcar_todas_leidas, name='marcar_todas_leidas'),
]