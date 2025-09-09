from django.urls import path
from . import views

urlpatterns = [
    path('templates/', views.template_list, name='template_list'),
    path('templates/upload/', views.upload_template, name='upload_template'),
    path('delete-template/<int:template_id>/', views.delete_template, name='delete_template'),
    path('templates/edit/<int:template_id>/', views.edit_template, name='edit_template'),

    # path('update-field-position/', views.update_field_position, name='update_field_position'),
]

