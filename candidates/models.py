# from django.db import models
# from django.conf import settings


# class Candidate(models.Model):
#     company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     course_title = models.CharField(max_length=200)
#     college = models.CharField(max_length=200)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)

#     def __str__(self):
#         return self.name


from django.db import models
from django.conf import settings
import uuid

class Candidate(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
      
    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=50)  # University Seat Number
    department = models.CharField(max_length=100)
    college = models.CharField(max_length=200)
    project_title = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.usn}"
