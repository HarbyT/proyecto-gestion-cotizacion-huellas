"""
URL configuration for huellas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from huellas import views  # importa la vista home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cuentas/', include('apps.cuentas.urls')),
    path('cuentas/', include('django.contrib.auth.urls')),  # <-- Agrega esta línea
    path('clientes/', include('apps.clientes.urls')),
    path('productos/', include('apps.productos.urls')),
    #path('api/materiales/', include('apps.materiales.urls')),
    #path('api/maquinas/', include('apps.maquinas.urls')),
    path('cotizaciones/', include('apps.cotizaciones.urls')),
    path('contacto/', views.enviar_contacto, name='enviar_contacto'),
    #path('api/reportes/', include('apps.reportes.urls')),
    path('notificaciones/', include('apps.notificaciones.urls')),

# Autenticación
    #path('accounts/login/', views.login_view, name='login'),
    #path('accounts/logout/', views.logout_view, name='logout'),
    #path('accounts/registro/', views.registro_view, name='registro'),
]
