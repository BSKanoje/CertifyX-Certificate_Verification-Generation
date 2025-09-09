from django.urls import path
from . import views

urlpatterns = [
    path('', views.candidate_list, name='candidate_list'),
    path('add/', views.candidate_create, name='candidate_create'),
    path('edit/<int:pk>/', views.candidate_edit, name='candidate_edit'),
    path('delete/<int:pk>/', views.candidate_delete, name='candidate_delete'),
    path('upload/', views.upload_candidates, name='candidate_upload'),
]
