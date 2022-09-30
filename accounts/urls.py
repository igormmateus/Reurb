from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='index_login'),
    path('login/', views.login, name='index_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cadastro_usuario/', views.cadastro_usuario, name='cadastro_usuario'),
    path('logout/', views.logout, name='logout'),
]