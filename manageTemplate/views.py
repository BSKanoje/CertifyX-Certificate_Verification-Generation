# from django.shortcuts import render, redirect, get_object_or_404
# from .models import CertificateTemplate, DynamicField
# from .forms import CertificateTemplateForm, DynamicFieldForm
# from subscriptions.models import CompanySubscription
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages


# @login_required
# def upload_template(request):
#     subscription = get_object_or_404(CompanySubscription, company=request.user)

#     if CertificateTemplate.objects.filter(company=request.user).count() >= subscription.plan.template_limit:
#         messages.error(request, "You have reached your template upload limit for your current plan.")
#         return redirect('template_list')

#     if request.method == 'POST':
#         form = CertificateTemplateForm(request.POST, request.FILES)
#         if form.is_valid():
#             template = form.save(commit=False)
#             template.company = request.user
#             template.save()
#             messages.success(request, "Template uploaded successfully!")
#             return redirect('template_list')
#     else:
#         form = CertificateTemplateForm()

#     return render(request, 'manageTemplate/upload_template.html', {'form': form})

# # # views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import CertificateTemplate, DynamicField
# from .forms import DynamicFieldForm

# def manage_fields(request, template_id):
#     template = get_object_or_404(CertificateTemplate, id=template_id)
#     form = DynamicFieldForm(request.POST or None)
#     fields = template.fields.all()

#     # Convert .pdf to .png if needed
#     image_url = template.preview_image.url if template.preview_image else ""  # assumes png already exists

#     if request.method == 'POST' and form.is_valid():
#         field_name = form.cleaned_data['field_name']
        
#         # Check if a field with the same name already exists
#         existing = template.fields.filter(field_name=field_name).first()
#         if existing:
#             # Update existing field instead of creating a new one
#             existing.font = form.cleaned_data['font']
#             existing.font_size = form.cleaned_data['font_size']
#             existing.position_x = form.cleaned_data['position_x']
#             existing.position_y = form.cleaned_data['position_y']
#             existing.save()
#         else:
#             # Save new field
#             new_field = form.save(commit=False)
#             new_field.template = template
#             new_field.save()

#         return redirect('manage_fields', template_id=template.id)

#     return render(request, 'manageTemplate/manage_fields.html', {
#         'form': form,
#         'fields': fields,
#         'template': template,
#         'image_url': image_url,
#     })



# from django.contrib import messages

# def template_list(request):
#     user = request.user
#     subscription = user.subscription  # Adjust if needed

#     templates = CertificateTemplate.objects.filter(company=user)
#     template_count = templates.count()
#     template_limit = subscription.plan.template_limit if subscription and subscription.plan else 0

#     if request.method == 'POST':
#         if template_count >= template_limit:
#             messages.error(request, "Template upload limit reached. Upgrade your plan to upload more.")
#             return redirect('template_list')

#         form = CertificateTemplateForm(request.POST, request.FILES)
#         if form.is_valid():
#             template = form.save(commit=False)
#             template.company = request.user
#             template.save()
#             messages.success(request, "Template uploaded successfully.")
#             return redirect('template_list')
#     else:
#         form = CertificateTemplateForm()

#     return render(request, 'manageTemplate/template_list.html', {
#         'form': form, 
#         'templates': templates, 
#         'subscription': subscription,
#         'template_limit': template_limit,
#         'template_count': template_count,
#         })






from django.shortcuts import render, redirect, get_object_or_404
from .models import CertificateTemplate
from .forms import CertificateTemplateForm
from subscriptions.models import CompanySubscription
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from PIL import Image, ImageDraw, ImageFont
import time
from django.conf import settings



# @login_required
# def upload_template(request):
#     subscription = get_object_or_404(CompanySubscription, company=request.user)

#     if CertificateTemplate.objects.filter(company=request.user).count() >= subscription.plan.template_limit:
#         messages.error(request, "You have reached your template upload limit for your current plan.")
#         return redirect('template_list')

#     if request.method == 'POST':
#         form = CertificateTemplateForm(request.POST, request.FILES)
#         if form.is_valid():
#             template = form.save(commit=False)
#             template.company = request.user
#             template.save()
#             messages.success(request, "Template uploaded successfully!")
#             return redirect('template_list')
#     else:
#         form = CertificateTemplateForm()

#     return render(request, 'manageTemplate/upload_template.html', {'form': form})


@login_required
def upload_template(request):
    subscription = get_object_or_404(CompanySubscription, company=request.user)

    if CertificateTemplate.objects.filter(company=request.user).count() >= subscription.plan.template_limit:
        messages.error(request, "You have reached your template upload limit for your current plan.")
        return redirect('template_list')

    if request.method == 'POST':
        form = CertificateTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            template = form.save(commit=False)
            template.company = request.user
            template.save()
            messages.success(request, f"{template.get_certificate_type_display()} uploaded successfully!")
            return redirect('template_list')
    else:
        form = CertificateTemplateForm()

    return render(request, 'manageTemplate/upload_template.html', {'form': form})



# def template_list(request):
#     user = request.user
#     subscription = user.subscription

#     templates = CertificateTemplate.objects.filter(company=user)
#     template_count = templates.count()
#     template_limit = subscription.plan.template_limit if subscription and subscription.plan else 0

#     if request.method == 'POST':
#         if template_count >= template_limit:
#             messages.error(request, "Template upload limit reached. Upgrade your plan to upload more.")
#             return redirect('template_list')

#         form = CertificateTemplateForm(request.POST, request.FILES)
#         if form.is_valid():
#             template = form.save(commit=False)
#             template.company = request.user
#             template.save()
#             messages.success(request, "Template uploaded successfully.")
#             return redirect('template_list')
#     else:
#         form = CertificateTemplateForm()

#     return render(request, 'manageTemplate/template_list.html', {
#         'form': form, 
#         'templates': templates, 
#         'subscription': subscription,
#         'template_limit': template_limit,
#         'template_count': template_count,
#     })

from django.core.paginator import Paginator

# def template_list(request):
#     user = request.user
#     subscription = getattr(user, 'subscription', None)

#     templates = CertificateTemplate.objects.filter(company=user)
#     template_count = templates.count()
#     template_limit = subscription.plan.template_limit if subscription and subscription.plan else 0

#     if request.method == 'POST':
#         if template_count >= template_limit:
#             messages.error(request, "Template upload limit reached. Upgrade your plan to upload more.")
#             return redirect('template_list')

#         form = CertificateTemplateForm(request.POST, request.FILES)
#         if form.is_valid():
#             template = form.save(commit=False)
#             template.company = request.user
#             template.save()
#             messages.success(request, f"{template.get_certificate_type_display()} uploaded successfully.")
#             return redirect('template_list')
#     else:
#         form = CertificateTemplateForm()

#     # ✅ Pagination here
#     paginator = Paginator(templates, 5)  # 5 per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'manageTemplate/template_list.html', {
#         'form': form,
#         'page_obj': page_obj,  # ✅ pass paginated object
#         'subscription': subscription,
#         'template_limit': template_limit,
#         'template_count': template_count,
#     })

def template_list(request):
    user = request.user
    subscription = getattr(user, 'subscription', None)

    # Get search query
    query = request.GET.get('q', '')

    # Base queryset
    templates = CertificateTemplate.objects.filter(company=user, is_deleted=False)


    # Apply search filter if query exists
    if query:
        templates = templates.filter(name__icontains=query)

    template_count = templates.count()
    template_limit = subscription.plan.template_limit if subscription and subscription.plan else 0

    if request.method == 'POST':
        if template_count >= template_limit:
            messages.error(request, "Template upload limit reached. Upgrade your plan to upload more.")
            return redirect('template_list')

        form = CertificateTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            template = form.save(commit=False)
            template.company = request.user
            template.save()
            messages.success(request, f"{template.get_certificate_type_display()} uploaded successfully.")
            return redirect('template_list')
    else:
        form = CertificateTemplateForm()

    # ✅ Pagination with search query preserved
    paginator = Paginator(templates, 5)  # 5 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'manageTemplate/template_list.html', {
        'form': form,
        'page_obj': page_obj,
        'subscription': subscription,
        'template_limit': template_limit,
        'template_count': template_count,
        'query': query,  # Pass query to template so input keeps value
    })


# from django.core.paginator import Paginator
# from django.shortcuts import render, redirect
# from django.contrib import messages

# def template_list(request):
#     user = request.user
#     subscription = getattr(user, 'subscription', None)

#     templates = CertificateTemplate.objects.filter(company=user).order_by('-id')
#     template_count = templates.count()
#     template_limit = subscription.plan.template_limit if subscription and subscription.plan else 0

#     if request.method == 'POST':
#         if template_count >= template_limit:
#             messages.error(request, "Template upload limit reached. Upgrade your plan to upload more.")
#             return redirect('template_list')

#         form = CertificateTemplateForm(request.POST, request.FILES)
#         if form.is_valid():
#             template = form.save(commit=False)
#             template.company = request.user
#             template.save()
#             messages.success(request, f"{template.get_certificate_type_display()} uploaded successfully.")
#             return redirect('template_list')
#     else:
#         form = CertificateTemplateForm()

#     # Pagination
#     paginator = Paginator(templates, 5)  # Show 5 templates per page
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'manageTemplate/template_list.html', {
#         'form': form, 
#         'page_obj': page_obj,  # pass paginated object
#         'subscription': subscription,
#         'template_limit': template_limit,
#         'template_count': template_count,
#     })


import os
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import CertificateTemplate  # Replace with your actual model

# def delete_template(request, template_id):
#     template = get_object_or_404(CertificateTemplate, id=template_id)

#     if request.method == "POST":
#         # Get file path before deleting object
#         file_path = template.file.path  # assuming 'file' is the FileField

#         # Delete the object from DB
#         template.delete()

#         # Delete the file from filesystem
#         if os.path.exists(file_path):
#             os.remove(file_path)

#         messages.success(request, "Template and its file deleted successfully.")
#         return redirect('template_list')  # replace with your list view name

#     messages.error(request, "Invalid delete request.")
#     return redirect('template_list')


@login_required
def delete_template(request, template_id):
    template = get_object_or_404(CertificateTemplate, id=template_id, company=request.user)

    if request.method == "POST":
        template.is_deleted = True
        template.save()
        messages.success(request, f"{template.get_certificate_type_display()} marked as deleted.")
        return redirect('template_list')

    messages.error(request, "Invalid delete request.")
    return redirect('template_list')

# def delete_template(request, template_id):
#     template = get_object_or_404(CertificateTemplate, id=template_id)

#     if request.method == "POST":
#         file_path = template.file.path
#         cert_type = template.get_certificate_type_display()

#         template.delete()

#         if os.path.exists(file_path):
#             os.remove(file_path)

#         messages.success(request, f"{cert_type} deleted successfully.")
#         return redirect('template_list')

#     messages.error(request, "Invalid delete request.")
#     return redirect('template_list')




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CertificateTemplate
from .forms import CertificateTemplateForm

@login_required
def edit_template(request, template_id):
    template = get_object_or_404(CertificateTemplate, id=template_id, company=request.user)

    if request.method == "POST":
        form = CertificateTemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, "Template updated successfully.")
            return redirect('template_list')
    else:
        form = CertificateTemplateForm(instance=template)

    return render(request, 'manageTemplate/edit_template.html', {'form': form})
