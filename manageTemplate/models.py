from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

FONT_CHOICES = [
    ('Times-Roman', 'Times New Roman'),
    ('Helvetica', 'Helvetica'),
    ('Courier', 'Courier New'),
]

CERTIFICATE_TYPE_CHOICES = [
    ('offer_letter', 'Offer Letter'),
    ('intermediate_letter', 'Intermediate Letter'),
    ('completion_certificate', 'Completion Certificate'),
    ('social_media', 'Social Media'),
]

class CertificateTemplate(models.Model):
    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    certificate_type = models.CharField(
        max_length=50,
        choices=CERTIFICATE_TYPE_CHOICES,
        default='offer_letter',
    )
    file = models.FileField(
        upload_to='certificate_templates/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Soft delete flag
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the file first

    def __str__(self):
        return f"{self.name} - {self.company.company_name}"


# # from django.db import models
# # from django.conf import settings
# # from django.core.validators import FileExtensionValidator
# # from pdf2image import convert_from_path
# # from PIL import Image
# # import os, uuid


# # FONT_CHOICES = [
# #     ('Times-Roman', 'Times New Roman'),
# #     ('Helvetica', 'Helvetica'),
# #     ('Courier', 'Courier New'),
# # ]

# # class CertificateTemplate(models.Model):
# #     company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# #     name = models.CharField(max_length=100)
# #     file = models.FileField(
# #                 upload_to='certificate_templates/',
# #                 validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
# #                 null=True,
# #                 blank=True,
# #             )
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     def save(self, *args, **kwargs):
# #         super().save(*args, **kwargs)  # Save the PDF first

# #     def __str__(self):
# #         return f"{self.name} - {self.company.company_name}"



# from django.db import models
# from django.conf import settings
# from django.core.validators import FileExtensionValidator

# FONT_CHOICES = [
#     ('Times-Roman', 'Times New Roman'),
#     ('Helvetica', 'Helvetica'),
#     ('Courier', 'Courier New'),
# ]

# CERTIFICATE_TYPE_CHOICES = [
#     ('offer_letter', 'Offer Letter'),
#     ('intermediate_letter', 'Intermediate Letter'),
#     ('completion_certificate', 'Completion Certificate'),
#     ('social_media', 'Social Media'),
# ]

# class CertificateTemplate(models.Model):
#     company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     certificate_type = models.CharField(
#         max_length=50,
#         choices=CERTIFICATE_TYPE_CHOICES,
#         default='offer_letter',
#     )
#     file = models.FileField(
#         upload_to='certificate_templates/',
#         validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
#         null=True,
#         blank=True,
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)  # Save the file first

#     def __str__(self):
#         return f"{self.name} - {self.company.company_name}"
