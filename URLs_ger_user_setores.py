from django.urls import path
from . import views

urlpatterns = [
    # URLs de Usuários
    path('usuarios/', views.user_list, name='user_list'),
    path('usuarios/novo/', views.user_create, name='user_create'),
    path('usuarios/editar/<int:pk>/', views.user_update, name='user_update'),
    path('usuarios/excluir/<int:pk>/', views.user_delete, name='user_delete'),
    
    # URLs de Setores
    path('setores/', views.SectorListView.as_view(), name='sector_list'),
    path('setores/novo/', views.SectorCreateView.as_view(), name='sector_create'),
    path('setores/editar/<int:pk>/', views.SectorUpdateView.as_view(), name='sector_update'),
    path('setores/excluir/<int:pk>/', views.SectorDeleteView.as_view(), name='sector_delete'),
]

