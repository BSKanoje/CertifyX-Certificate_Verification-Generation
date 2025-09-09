from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator # Import for file validation

class CompanyManager(BaseUserManager):
    def create_user(self, email, company_name, phone, password=None):
        if not email:
            raise ValueError("Companies must have an email address")
        email = self.normalize_email(email)
        company = self.model(email=email, company_name=company_name, phone=phone)
        company.set_password(password)
        company.save(using=self._db)
        return company

    def create_superuser(self, email, company_name, phone, password):
        company = self.create_user(email, company_name, phone, password)
        company.is_staff = True
        company.is_superuser = True
        company.save(using=self._db)
        return company

class Company(AbstractBaseUser, PermissionsMixin):
    company_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    logo = models.ImageField(
        upload_to='company_logos/',
        null=True,
        blank=True,
        help_text="Company logo (PNG, JPG, SVG)",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])]
    )
    address = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name', 'phone']

    objects = CompanyManager()

    def __str__(self):
        return self.company_name
