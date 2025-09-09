from django.db import models
from django.conf import settings
from datetime import date, timedelta
from generateCertificate.models import Certificate

class PricingPlan(models.Model):
    name = models.CharField(max_length=50)
    certificate_limit = models.PositiveIntegerField()
    template_limit = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    validity_period = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name


class CompanySubscription(models.Model):
    company = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription")
    plan = models.ForeignKey(PricingPlan, on_delete=models.SET_NULL, null=True)
    certificates_used = models.PositiveIntegerField(default=0)
    start_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)  # Track active status
    next_plan = models.CharField(max_length=100, blank=True, null=True)  # Store upgraded plan if applicable
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Failed', 'Failed')], default='Pending')
    payment_reference = models.CharField(max_length=100, null=True, blank=True)

    def is_subscription_active(self):
        return self.expiry_date >= date.today()
    
    def get_certificates_used(self):
        return Certificate.objects.filter(company=self.company).count()

    def remaining_certificates(self):
        if not self.plan:
            return 0
        used = Certificate.objects.filter(company=self.company).count()
        return self.plan.certificate_limit - used
    
    def renew(self, days=30):
        self.expiry_date = self.expiry_date + timedelta(days=days)
        self.save()

    def upgrade_plan(self, new_plan: PricingPlan):
        if new_plan != self.plan:
            self.plan = new_plan
            self.next_plan = new_plan.name  
            self.expiry_date = date.today() + timedelta(days=new_plan.validity_period)  
            self.save()

    def __str__(self):
        return f"{self.company.company_name} - {self.plan.name if self.plan else 'No Plan'}"
