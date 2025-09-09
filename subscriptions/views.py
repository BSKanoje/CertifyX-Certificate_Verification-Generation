from django.contrib.auth.decorators import login_required
from .models import PricingPlan, CompanySubscription
from datetime import date, timedelta
from django.utils import timezone
from django.utils.crypto import get_random_string
from .services import get_new_plan_price  
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages


@login_required
def choose_plan(request, id):
    plan = PricingPlan.objects.get(id=id)

    try:
        subscription = CompanySubscription.objects.get(company=request.user)
    except CompanySubscription.DoesNotExist:
        subscription = None

    if subscription:
        if subscription.plan != plan:
            subscription.plan = plan
            subscription.expiry_date = date.today() + timedelta(days=30) 

    else:
        subscription = CompanySubscription(company=request.user)
        subscription.plan = plan
        subscription.certificates_used = 0  
        subscription.start_date = date.today()
        subscription.expiry_date = timezone.now() + timedelta(days=30)  

    subscription.save()

    return redirect('mock_payment', plan_id=plan.id)  



@login_required
def plans_view(request):
    user = request.user

    try:
        subscription = CompanySubscription.objects.get(company=user)
        certificates_used = subscription.get_certificates_used()
        remaining_certificates = subscription.remaining_certificates()
    except CompanySubscription.DoesNotExist:
        subscription = None
        certificates_used = 0
        remaining_certificates = 0

    plans = PricingPlan.objects.all()

    context = {
        'company': user,
        'subscription': subscription,
        'plans': plans,
        'certificates_used': certificates_used,
        'remaining_certificates': remaining_certificates
    }

    return render(request, 'plans.html', context)


@login_required
def confirm_payment(request, plan_id):
    plan = PricingPlan.objects.get(id=plan_id)
    subscription, created = CompanySubscription.objects.get_or_create(company=request.user)

    subscription.payment_status = 'Paid'  
    subscription.save()

    return redirect('home')


@login_required
def mock_payment(request, plan_id):
    plan = get_object_or_404(PricingPlan, id=plan_id)
    subscription, created = CompanySubscription.objects.get_or_create(
        company=request.user,
        defaults={
        'plan': plan, 
        'start_date': timezone.now(),
        'expiry_date': timezone.now() + timedelta(days=30),
        }
        )

    if request.method == "POST":
        subscription.plan = plan
        subscription.payment_status = 'Paid'
        subscription.payment_reference = get_random_string(12).upper()
        subscription.start_date = date.today()
        subscription.expiry_date = date.today() + timedelta(days=30)
        subscription.save()
        return redirect('payment_success', id=plan.id)

    return render(request, 'mock_payment.html', {'plan': plan})

@login_required
def payment_success(request, id=None):
    plan = PricingPlan.objects.get(id=id)
    return render(request, 'payment_success.html', {'plan': plan})


def renew_subscription(request, subscription_id):
    subscription = get_object_or_404(CompanySubscription, id=subscription_id)

    if request.method == 'POST':
        if subscription.is_subscription_active():
            subscription.renew(30)
            messages.success(request, f"Your subscription has been renewed. New expiry date: {subscription.expiry_date}")
        else:
            messages.error(request, "Your subscription is not active and cannot be renewed.")
        return redirect('renew', subscription_id=subscription_id)  
    return render(request, 'renew.html', {
        'subscription': subscription
    })

def upgrade_plan(request, subscription_id, plan_name):
    subscription = get_object_or_404(CompanySubscription, id=subscription_id)
    plans = PricingPlan.objects.all()

    if request.method == 'POST':
        selected_plan_id = request.POST.get('plan')
        selected_plan = get_object_or_404(PricingPlan, id=selected_plan_id)

        if selected_plan != subscription.plan:
            subscription.upgrade_plan(selected_plan)
            messages.success(request, f"Successfully upgraded to {selected_plan.name} plan.")
        else:
            messages.info(request, "You are already on this plan.")

        return redirect('upgrade_plan', subscription_id=subscription.id, plan_name=selected_plan.name)

    return render(request, 'upgrade_plan.html', {
        'subscription': subscription,
        'plan_name': plan_name,
        'plans': plans
    })
