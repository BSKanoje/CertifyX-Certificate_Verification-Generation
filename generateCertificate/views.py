# views.py

from datetime import date
import os
import tempfile
import urllib.parse
import pythoncom

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import FileResponse
from django.core.paginator import Paginator
from django.db.models import Q

from docx2pdf import convert

from .models import CertificateTemplate, Certificate, Candidate, CERTIFICATE_TYPE_CHOICES
from .utils import get_pronouns, generate_certificate_docx
from subscriptions.models import CompanySubscription

@login_required
def generate_certificates(request):
    if request.method == 'POST':
        template_id = request.POST.get('template')
        candidate_ids = request.POST.getlist('candidates')

        if not template_id or not candidate_ids:
            messages.error(request, 'Template and candidates must be selected.')
            return redirect('generate_certificates')

        try:
            template = CertificateTemplate.objects.get(id=template_id, company=request.user)
        except CertificateTemplate.DoesNotExist:
            messages.error(request, 'Invalid template selection.')
            return redirect('generate_certificates')

        candidates = Candidate.objects.filter(id__in=candidate_ids, company=request.user)

        # Check company subscription
        try:
            subscription = CompanySubscription.objects.get(company=request.user)
        except CompanySubscription.DoesNotExist:
            messages.error(request, "No active subscription found.")
            return redirect('home')

        if not subscription.is_subscription_active():
            messages.error(request, "Your subscription has expired.")
            return redirect('home')

        remaining = subscription.remaining_certificates()
        if len(candidates) > remaining:
            messages.error(request, f"Only {remaining} certificates can be generated under your current plan.")
            return redirect('generate_certificates')

        # Generate certificates
        for candidate in candidates:
            # ... inside your loop
            uid, docx_buffer = generate_certificate_docx(template, candidate)

            # Create a temporary DOCX file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
                temp_docx.write(docx_buffer.read())
                temp_docx_path = temp_docx.name

            # Convert to PDF
            temp_pdf_path = temp_docx_path.replace(".docx", ".pdf")
            pythoncom.CoInitialize()  # Initialize COM
            try:
                convert(temp_docx_path, temp_pdf_path)
            finally:
                pythoncom.CoUninitialize()

            # Read the PDF content
            with open(temp_pdf_path, "rb") as pdf_file:
                pdf_content = pdf_file.read()

            # Save to Certificate model
            Certificate.objects.create(
                candidate=candidate,
                template=template,
                company=request.user,
                unique_id=uid,
                pdf_file=ContentFile(pdf_content, name=f"{uid}.pdf"),
            )

            # Clean up temp files
            os.remove(temp_docx_path)
            os.remove(temp_pdf_path)

        # Update certificate usage
        subscription.certificates_used += len(candidates)
        subscription.save()

        messages.success(request, f"{len(candidates)} certificate(s) generated successfully!")
        return redirect('certificate_list')

    # GET request handling
    templates = CertificateTemplate.objects.filter(company=request.user)
    candidates = Candidate.objects.filter(company=request.user)

    # Search
    query = request.GET.get('q')
    if query:
        candidates = candidates.filter(
            Q(name__icontains=query) |
            Q(usn__icontains=query) |
            Q(department__icontains=query) |
            Q(college__icontains=query) |
            Q(project_title__icontains=query)
        )

    # Pagination
    paginator = Paginator(candidates, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'generateCertificate/generate.html', {
        'templates': templates,
        'candidates': page_obj,   
        'page_obj': page_obj,
        'query': query,
        "CERTIFICATE_TYPE_CHOICES": CERTIFICATE_TYPE_CHOICES,
    })


def verify_certificate(request):
    context = {}
    
    if request.method == 'POST':
        cert_id = request.POST.get('certificate_id')

        if cert_id:
            try:
                certificate = Certificate.objects.select_related(
                    'candidate', 'template', 'company'
                ).get(unique_id=cert_id)

                status = "Valid"

                context['certificate'] = {
                    'student_name': certificate.candidate.name,
                    'project_title': certificate.candidate.project_title,  # ✅ Candidate field
                    'company_name': certificate.company.company_name,
                    'certificate_type': certificate.template.get_certificate_type_display(),  # ✅ From Template
                    'start_date': certificate.candidate.start_date.strftime('%B %d, %Y'),
                    'end_date': certificate.candidate.end_date.strftime('%B %d, %Y'),
                    'issue_date': certificate.issue_date.strftime('%B %d, %Y'),
                    'status': status
                }
            except Certificate.DoesNotExist:
                context['error'] = "Invalid Certificate ID."

    return render(request, 'generateCertificate/verify_certificate.html', context)


@login_required
def certificate_list(request):
    # Get all certificates for current company
    certificates = Certificate.objects.filter(
        candidate__company=request.user
    ).select_related('candidate', 'template')

    # Group certificates by candidate
    candidates = {}
    for cert in certificates:
        cand_id = cert.candidate.id
        if cand_id not in candidates:
            candidates[cand_id] = {
                'candidate': cert.candidate,
                'certificates': {}
            }
        # Use template.certificate_type as key
        candidates[cand_id]['certificates'][cert.template.certificate_type] = cert

    # Convert to list for pagination
    candidate_list = list(candidates.values())
    paginator = Paginator(candidate_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    CERTIFICATE_TYPES = [
    ('offer_letter', 'Offer Letter'),
    ('intermediate_letter', 'Intermediate Letter'),
    ('completion_certificate', 'Completion Letter'),
    ('social_media', 'Social Media Certificate'),
]
    return render(request, 'generateCertificate/certificate_list.html', {
        'candidate_list': page_obj,
        'page_obj': page_obj,
        'certificate_types': CERTIFICATE_TYPES,
    })


def send_certificate_email(request, cert_id):
    cert = get_object_or_404(Certificate, id=cert_id)
    resend = request.GET.get('resend', 'false').lower() == 'true'

    if cert.email_sent and not resend:
        messages.warning(request, f"Email already sent to {cert.candidate.name}.")
        return redirect('generated_certificates')

    try:

        company_name = cert.company.company_name

        email = EmailMessage(
            subject='Your Internship Certificate',
            body=f"Dear {cert.candidate.name},\n\nPlease find attached your internship certificate as a token of appreciation for your valuable contributions during your internship with us.\n\nWishing you continued success in your future endeavors!\n\nRegards,\nTeam {company_name}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[cert.candidate.email],
        )

        email.attach_file(cert.pdf_file.path)
        email.send()

        cert.email_sent = True  # remains True even on resend
        cert.save()

        if resend:
            messages.success(request, f"Certificate resent successfully to {cert.candidate.email}.")
        else:
            messages.success(request, f"Certificate sent successfully to {cert.candidate.email}.")

    except Exception as e:
        print(e)
        messages.error(request, "An error occurred while sending the email.")

    return redirect('certificate_list')


@login_required
def download_certificate(request, cert_id):
    cert = get_object_or_404(Certificate, id=cert_id, candidate__company=request.user)

    student_name = cert.candidate.name.replace(" ", "")  # Remove spaces
    template_type = cert.template.get_certificate_type_display().replace(" ", "_")  # e.g. "Offer Letter" → "Offer_Letter"
    filename = f"{student_name}_{template_type}.pdf"

    response = FileResponse(open(cert.pdf_file.path, 'rb'), content_type='application/pdf')
    # Use Content-Disposition to force download with custom filename
    response['Content-Disposition'] = f'attachment; filename="{urllib.parse.quote(filename)}"'
    return response
