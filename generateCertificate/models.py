import uuid
from django.db import models
from django.conf import settings
from candidates.models import *
from manageTemplate.models import *
from accounts.models import Company

class Certificate(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    template = models.ForeignKey(CertificateTemplate, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    email_sent = models.BooleanField(default=False) 

    def __str__(self):
        return f"Certificate for {self.candidate.name}"
