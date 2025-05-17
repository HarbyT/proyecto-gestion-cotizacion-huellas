from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def perfil(request):
    perfil = None
    if hasattr(request.user, 'perfil'):
        perfil = request.user.perfil
    return render(request, 'cuentas/perfil.html', {'perfil': perfil})