from django.urls import path
from . import views  

urlpatterns = [
    path('renew/<int:subscription_id>/', views.renew_subscription, name='renew'),

    path('upgrade_plan/<int:subscription_id>/<str:plan_name>/', views.upgrade_plan, name='upgrade_plan'),
]
