from django.urls import path
from . import views

urlpatterns = [
    path('precadastro/', views.precadastro, name='precadastro'),
    path('busca/', views.busca, name='busca'),
    path('<int:imovel_id>', views.ver_imovel, name='ver_imovel'),
    path('index', views.Index.as_view(), name='index'),
    path('', views.cadastro_beneficiario, name='cadastro_beneficiario'),
    path('conjugue/<int:pk>', views.CadastroConjugue.as_view(), name='conjugue'),
]
