from django.urls import path
from . import views

urlpatterns = [
    path('docx/<int:pk>', views.ExportDocx.as_view(), name='gera_docx')
]