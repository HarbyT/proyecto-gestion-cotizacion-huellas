from django.urls import path
from .views import ClienteList, ClienteDetail, ClienteCreate, ClienteUpdate, ClienteDelete
urlpatterns = [
    path('', ClienteList.as_view(), name='cliente_list'),
    path('<int:pk>/', ClienteDetail.as_view(), name='cliente_detail'),
    path('nuevo/', ClienteCreate.as_view(), name='cliente_create'),
    path('<int:pk>/editar/', ClienteUpdate.as_view(), name='cliente_update'),
    path('<int:pk>/eliminar/', ClienteDelete.as_view(), name='cliente_delete'),
]
