from django.urls import path
from . import views

app_name = 'pdf_merger_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('merge/', views.merge_pdfs, name='merge_pdfs'),
]
