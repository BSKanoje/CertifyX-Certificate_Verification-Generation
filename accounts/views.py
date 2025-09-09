from django.shortcuts import render, redirect
from .models import Company
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from datetime import date
from subscriptions.models import CompanySubscription, PricingPlan
from .forms import CompanyProfileUpdateForm # Import the form for profile updates
from generateCertificate.models import Certificate  # Add this at the top with other imports


def about(request):
    return render(request, 'about.html')


def home_view(request):
    user = request.user

    try:
        subscription = CompanySubscription.objects.get(company=user)
        days_left = (subscription.expiry_date - date.today()).days if subscription.expiry_date else 0
        certificates_used = subscription.get_certificates_used()  # Get accurate count
        remaining_certificates = subscription.remaining_certificates()
    except CompanySubscription.DoesNotExist:
        subscription = None
        days_left = 0
        certificates_used = 0
        remaining_certificates = 0

    plans = PricingPlan.objects.all()

    context = {
        'company': user,
        'subscription': subscription,
        'plans': plans,
        'days_left': days_left,
        'certificates_used': certificates_used,
        'remaining_certificates': remaining_certificates
    }

    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        company_name = request.POST['company_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        if Company.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        if Company.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already registered.')
            return redirect('register')

        company = Company.objects.create(
            company_name=company_name,
            email=email,
            phone=phone,
            password=make_password(password) 
        )
        login(request, company)
        return redirect('home')  

    return render(request, 'register.html')

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('login')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('/')



@login_required
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset-password')  

        user = request.user
        user.set_password(new_password) 
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully.")

    return render(request, 'reset_password.html')


@login_required
def profile_settings(request):
    company = request.user 

    if request.method == 'POST':
        form = CompanyProfileUpdateForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile-settings')
    else:
        form = CompanyProfileUpdateForm(instance=company)

    # Fetch subscription details to display (Section 8 requirement)
    try:
        subscription = CompanySubscription.objects.get(company=company)
        days_left = (subscription.expiry_date - date.today()).days if subscription.expiry_date else 0
        remaining_certificates = subscription.remaining_certificates()
    except CompanySubscription.DoesNotExist:
        subscription = None
        days_left = 0
        remaining_certificates = 0

    context = {
        'form': form,
        'company': company,
        'subscription': subscription,
        'days_left': days_left,
        'remaining_certificates': remaining_certificates,
    }
    return render(request, 'profile_settings.html', context)

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.utils import timezone
# from datetime import timedelta
# import json
# from django.utils.safestring import mark_safe
# from generateCertificate.models import Certificate
# from subscriptions.models import CompanySubscription

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.utils import timezone
# from datetime import timedelta
# import json
# from django.utils.safestring import mark_safe
# from collections import Counter

# @login_required
# def reports_view(request):
#     user = request.user

#     try:
#         subscription = CompanySubscription.objects.get(company=user)
#         certificates_used = subscription.get_certificates_used()
#         certificate_limit = subscription.plan.certificate_limit
#         days_left = (subscription.expiry_date - timezone.now().date()).days
#         is_active = subscription.is_subscription_active()
#     except CompanySubscription.DoesNotExist:
#         subscription = None
#         certificates_used = 0
#         certificate_limit = 0
#         days_left = 0
#         is_active = False

#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     template_name = request.GET.get('template')

#     filtered_certificates = Certificate.objects.filter(company=user)

#     if start_date:
#         filtered_certificates = filtered_certificates.filter(issue_date__gte=start_date)
#     if end_date:
#         filtered_certificates = filtered_certificates.filter(issue_date__lte=end_date)
#     if template_name:
#         filtered_certificates = filtered_certificates.filter(template__name__iexact=template_name)

#     recent_certificates = filtered_certificates.order_by('-issue_date')[:5]

#     total_certificates = filtered_certificates.count()  # Only filtered count

#     # Prepare chart data (last 7 days) from filtered data
#     today = timezone.now().date()
#     usage_dates = []
#     usage_counts = []

#     for i in range(7):
#         day = today - timedelta(days=i)
#         usage_dates.append(day.strftime('%b %d'))
#         count = filtered_certificates.filter(issue_date=day).count()
#         usage_counts.append(count)

#     usage_dates.reverse()
#     usage_counts.reverse()

#     # Template Usage Pie Chart from filtered data
#     from collections import Counter
#     template_data = filtered_certificates.values_list('template__name', flat=True)
#     template_count = dict(Counter(template_data))
#     template_labels = list(template_count.keys())
#     template_values = list(template_count.values())

#     # Top Candidates and Templates from filtered data
#     from django.db.models import Count

#     top_candidates = filtered_certificates\
#         .values('candidate__name')\
#         .annotate(count=Count('id'))\
#         .order_by('-count')[:5]

#     top_templates = filtered_certificates\
#         .values('template__name')\
#         .annotate(count=Count('id'))\
#         .order_by('-count')[:5]

#     context = {
#         'total_certificates': total_certificates,
#         'certificates_used': certificates_used,
#         'certificate_limit': certificate_limit,
#         'subscription': subscription,
#         'days_left': days_left,
#         'recent_certificates': recent_certificates,

#         'usage_dates': usage_dates,
#         'usage_counts': usage_counts,
#         'template_labels': template_labels,
#         'template_counts': template_count,

#         'usage_dates_json': mark_safe(json.dumps(usage_dates)),
#         'usage_counts_json': mark_safe(json.dumps(usage_counts)),
#         'template_labels_json': mark_safe(json.dumps(template_labels)),
#         'template_values_json': mark_safe(json.dumps(template_values)),

#         'top_candidates': top_candidates,
#         'top_templates': top_templates,
#     }

#     return render(request, 'reports.html', context)



# import csv
# from django.http import HttpResponse

# @login_required
# def export_certificates_csv(request):
#     user = request.user
#     certificates = Certificate.objects.filter(company=user).order_by('-issue_date')

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="certificates.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['Candidate Name', 'Issue Date', 'Template'])

#     for cert in certificates:
#         writer.writerow([cert.candidate.name, cert.issue_date, cert.template.name])

#     return response


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.utils import timezone
# from datetime import timedelta
# import json
# from manageTemplate.models import CertificateTemplate
# from django.utils.safestring import mark_safe
# from collections import Counter
# from django.db.models import Count
# from generateCertificate.models import Certificate
# from subscriptions.models import CompanySubscription

# @login_required
# def reports_view(request):
#     user = request.user

#     try:
#         subscription = CompanySubscription.objects.get(company=user)
#         certificates_used = subscription.get_certificates_used()
#         certificate_limit = subscription.plan.certificate_limit
#         days_left = (subscription.expiry_date - timezone.now().date()).days
#         is_active = subscription.is_subscription_active()
#     except CompanySubscription.DoesNotExist:
#         subscription = None
#         certificates_used = 0
#         certificate_limit = 0
#         days_left = 0
#         is_active = False

#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     template_name = request.GET.get('template')

#     filtered_certificates = Certificate.objects.filter(company=user)

#     if start_date:
#         filtered_certificates = filtered_certificates.filter(issue_date__gte=start_date)
#     if end_date:
#         filtered_certificates = filtered_certificates.filter(issue_date__lte=end_date)
#     if template_name:
#         filtered_certificates = filtered_certificates.filter(template__name__iexact=template_name)

#     recent_certificates = filtered_certificates.order_by('-issue_date')[:5]
#     total_certificates = filtered_certificates.count()

#     today = timezone.now().date()
#     usage_dates, usage_counts = [], []
#     for i in range(7):
#         day = today - timedelta(days=i)
#         usage_dates.append(day.strftime('%b %d'))
#         usage_counts.append(filtered_certificates.filter(issue_date=day).count())

#     usage_dates.reverse()
#     usage_counts.reverse()

#     template_data = filtered_certificates.values_list('template__name', flat=True)
#     template_count = dict(Counter(template_data))
#     template_labels = list(template_count.keys())
#     template_values = list(template_count.values())

#     top_candidates = filtered_certificates.values('candidate__name').annotate(count=Count('id')).order_by('-count')[:5]
#     top_templates = filtered_certificates.values('template__name').annotate(count=Count('id')).order_by('-count')[:5]

#     # Certificate type counts
#     offer_letter_count = CertificateTemplate.objects.filter(company=user, certificate_type='offer_letter').count()
#     intermediate_count = CertificateTemplate.objects.filter(company=user, certificate_type='intermediate_letter').count()
#     completion_count = CertificateTemplate.objects.filter(company=user, certificate_type='completion_certificate').count()
#     social_media_count = CertificateTemplate.objects.filter(company=user, certificate_type='social_media').count()


#     context = {
#         'total_certificates': total_certificates,
#         'certificates_used': certificates_used,
#         'certificate_limit': certificate_limit,
#         'subscription': subscription,
#         'days_left': days_left,
#         'recent_certificates': recent_certificates,
#         'usage_dates_json': mark_safe(json.dumps(usage_dates)),
#         'usage_counts_json': mark_safe(json.dumps(usage_counts)),
#         'template_labels_json': mark_safe(json.dumps(template_labels)),
#         'template_values_json': mark_safe(json.dumps(template_values)),
#         'top_candidates': top_candidates,
#         'top_templates': top_templates,
#         'offer_letter_count': offer_letter_count,
#         'intermediate_count': intermediate_count,
#         'completion_count': completion_count,
#         'social_media_count': social_media_count,
#         'template_labels': template_labels,
#     }
#     return render(request, 'reports.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
import json
from manageTemplate.models import CertificateTemplate
from django.utils.safestring import mark_safe
from collections import Counter
from django.db.models import Count
from generateCertificate.models import Certificate
from subscriptions.models import CompanySubscription

@login_required
def reports_view(request):
    user = request.user

    # Subscription info
    try:
        subscription = CompanySubscription.objects.get(company=user)
        certificates_used = subscription.get_certificates_used()
        certificate_limit = subscription.plan.certificate_limit
        days_left = (subscription.expiry_date - timezone.now().date()).days
        is_active = subscription.is_subscription_active()
    except CompanySubscription.DoesNotExist:
        subscription = None
        certificates_used = 0
        certificate_limit = 0
        days_left = 0
        is_active = False

    # Filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    template_name = request.GET.get('template')

    filtered_certificates = Certificate.objects.filter(company=user)
    if start_date:
        filtered_certificates = filtered_certificates.filter(issue_date__gte=start_date)
    if end_date:
        filtered_certificates = filtered_certificates.filter(issue_date__lte=end_date)
    if template_name:
        filtered_certificates = filtered_certificates.filter(template__name__iexact=template_name)

    total_certificates = filtered_certificates.count()
    recent_certificates = filtered_certificates.order_by('-issue_date')[:5]

    # 7-day usage
    today = timezone.now().date()
    usage_dates, usage_counts = [], []
    for i in range(7):
        day = today - timedelta(days=i)
        usage_dates.append(day.strftime('%b %d'))
        usage_counts.append(filtered_certificates.filter(issue_date=day).count())
    usage_dates.reverse()
    usage_counts.reverse()

    # Template usage
    template_data = filtered_certificates.values_list('template__name', flat=True)
    template_count = dict(Counter(template_data))
    template_labels = list(template_count.keys())
    template_values = list(template_count.values())

    # Top candidates and templates
    top_candidates = filtered_certificates.values('candidate__name').annotate(count=Count('id')).order_by('-count')[:5]
    top_templates = filtered_certificates.values('template__name').annotate(count=Count('id')).order_by('-count')[:5]

    # Certificate type counts based on issued certificates
    certificate_type_counts = filtered_certificates.values('template__certificate_type').annotate(count=Count('id'))
    offer_letter_count = intermediate_count = completion_count = social_media_count = 0
    for item in certificate_type_counts:
        ctype = item['template__certificate_type']
        if ctype == 'offer_letter':
            offer_letter_count = item['count']
        elif ctype == 'intermediate_letter':
            intermediate_count = item['count']
        elif ctype == 'completion_certificate':
            completion_count = item['count']
        elif ctype == 'social_media':
            social_media_count = item['count']

    context = {
        'total_certificates': total_certificates,
        'certificates_used': certificates_used,
        'certificate_limit': certificate_limit,
        'subscription': subscription,
        'days_left': days_left,
        'recent_certificates': recent_certificates,
        'usage_dates_json': mark_safe(json.dumps(usage_dates)),
        'usage_counts_json': mark_safe(json.dumps(usage_counts)),
        'template_labels_json': mark_safe(json.dumps(template_labels)),
        'template_values_json': mark_safe(json.dumps(template_values)),
        'top_candidates': top_candidates,
        'top_templates': top_templates,
        'offer_letter_count': offer_letter_count,
        'intermediate_count': intermediate_count,
        'completion_count': completion_count,
        'social_media_count': social_media_count,
        'template_labels': template_labels,
    }

    return render(request, 'reports.html', context)

import csv
from django.http import HttpResponse

@login_required
def export_certificates_csv(request):
    user = request.user
    certificates = Certificate.objects.filter(company=user).order_by('-issue_date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="certificates.csv"'

    writer = csv.writer(response)
    writer.writerow(['Candidate Name', 'Issue Date', 'Template'])

    for cert in certificates:
        writer.writerow([cert.candidate.name, cert.issue_date, cert.template.name])

    return response
