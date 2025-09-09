from django.urls import path
from . import views

urlpatterns = [
    path('generate-certificate/', views.generate_certificates, name='generate_certificates'),
    path('verify/', views.verify_certificate, name='verify_certificate'),
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('send-mail/<int:cert_id>/', views.send_certificate_email, name='send_certificate_email'),
    path('download/<int:cert_id>/', views.download_certificate, name='download_certificate'),

]
