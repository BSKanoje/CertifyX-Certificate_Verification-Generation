"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import *
from django.conf.urls.static import static
from django.conf import settings
from subscriptions.views import *
from manageTemplate.views import *


urlpatterns = [
    path('', about),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('reset-password/', reset_password, name='reset-password'),

    path('profile-settings/', profile_settings, name='profile-settings'), # to update company profile

    path('plans/', plans_view, name='plans'),
    path('choose-plan/<int:id>/', choose_plan, name='choose_plan'),
    path('pay/<int:plan_id>/', mock_payment, name='mock_payment'),
    path('payment-success/<int:id>/', payment_success, name='payment_success'),
    path('reports/', reports_view, name='reports'),
    path('reports/export/csv/', export_certificates_csv, name='export-certificates-csv'),
# urls.py

    path('subscriptions/', include('subscriptions.urls')),
    path('manageTemplate/', include('manageTemplate.urls')),
    path('candidates/', include('candidates.urls')),
    path('generateCertificate/', include('generateCertificate.urls')),
    
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

