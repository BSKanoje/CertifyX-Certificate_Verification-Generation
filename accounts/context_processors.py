# accounts/context_processors.py
from candidates.models import Candidate

def total_students_processor(request):
    if request.user.is_authenticated:
        total_students = Candidate.objects.filter(company=request.user).count()
    else:
        total_students = 0
    return {'total_students': total_students}
