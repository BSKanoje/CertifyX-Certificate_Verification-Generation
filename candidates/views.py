import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidate
from .forms import CandidateForm, UploadFileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator


# @login_required
# def candidate_list(request):
#     query = request.GET.get('q')
#     candidates = Candidate.objects.filter(company=request.user)

#     if query:
#         candidates = candidates.filter(
#             Q(name__icontains=query) |
#             Q(college__icontains=query) |
#             Q(usn__icontains=query) |
#             Q(department__icontains=query) |
#             Q(project_title__icontains=query)
#         )

#     # Pagination
#     paginator = Paginator(candidates, 5)  # 5 candidates per page
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'candidates/candidate_list.html', {
#         'page_obj': page_obj,
#         'query': query,  # Optional: to preserve search term in template
#     })


@login_required
def candidate_create(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.company = request.user
            candidate.save()
            messages.success(request, 'Candidate added successfully!')
            return redirect('candidate_list')
    else:
        form = CandidateForm()
    return render(request, 'candidates/candidate_form.html', {'form': form})

@login_required
def candidate_list(request):
    query = request.GET.get('q', '')

    # Filter candidates for the logged-in user's company
    try:
        candidates = Candidate.objects.filter(company=request.user.company)
    except AttributeError:
        candidates = Candidate.objects.filter(company=request.user)  # fallback if company=user

    # Apply search filter
    if query:
        candidates = candidates.filter(
            Q(name__icontains=query) |
            Q(college__icontains=query) |
            Q(usn__icontains=query) |
            Q(department__icontains=query) |
            Q(project_title__icontains=query)
        )

    # Pagination
    paginator = Paginator(candidates, 5)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'candidates/candidate_list.html', {
        'page_obj': page_obj,
        'query': query,
    })

@login_required
def candidate_edit(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk, company=request.user)
    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate updated.')
            return redirect('candidate_list')
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'candidates/candidate_form.html', {'form': form})

@login_required
def candidate_delete(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk, company=request.user)
    if request.method == 'POST':
        candidate.delete()
        messages.success(request, 'Candidate deleted.')
        return redirect('candidate_list')
    return render(request, 'candidates/candidate_confirm_delete.html', {'candidate': candidate})

@login_required
def upload_candidates(request):
    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)

            # Clean column names
            df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

            # Define required columns
            required_columns = {
                'name', 'usn', 'department', 'college', 'project_title',
                'start_date', 'end_date', 'email', 'phone'
            }

            # Check for missing columns
            if not required_columns.issubset(df.columns):
                messages.error(
                    request,
                    f"Excel is missing required columns. Found: {', '.join(df.columns)}"
                )
                return redirect('candidate_upload')

            # Create Candidate objects
            for _, row in df.iterrows():
                try:
                    Candidate.objects.create(
                        company=request.user,
                        name=row['name'],
                        usn=row['usn'],
                        department=row['department'],
                        college=row['college'],
                        project_title=row['project_title'],
                        start_date=row['start_date'],
                        end_date=row['end_date'],
                        email=row['email'],
                        phone=str(row['phone']),
                    )
                except Exception as e:
                    messages.error(request, f"Error saving candidate: {e}")

            messages.success(request, 'Candidates uploaded successfully.')
            return redirect('candidate_list')
    else:
        form = UploadFileForm()

    context = {
        'form': form,
        'MEDIA_URL': settings.MEDIA_URL
    }  

    return render(request, 'candidates/upload.html', context)
