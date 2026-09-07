from django.db import models
from django.contrib.auth.models import User
from course.models import Course

class AdmissionApplication(models.Model):

    STUDENT_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    application_number = models.CharField(max_length=50, unique=True)
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STUDENT_CHOICES, default='Pending')

    def __str__(self):
        return self.application_number

class AcademicDetails(models.Model):
    application = models.OneToOneField(AdmissionApplication, on_delete=models.CASCADE)

    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    tenth_collage = models.CharField(max_length=100)
    tenth_board = models.CharField(max_length=100)
    tenth_passing_year = models.IntegerField()


    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    twelfth_collage = models.CharField(max_length=100)
    twelfth_board = models.CharField(max_length=100)
    twelfth_passing_year = models.IntegerField()

    def __str__(self):
        return self.application.application_number

class StudentDocuments(models.Model):
    application = models.OneToOneField(AdmissionApplication, on_delete=models.CASCADE)

    photo = models.ImageField(upload_to='documents/photos/')
    signature = models.ImageField(upload_to='documents/signature/')
    tenth_marksheet = models.ImageField(upload_to='documents/tenth_marksheet/')
    twelfth_marksheet = models.ImageField(upload_to='documents/twelth_marksheet/')
    leaving_certificate = models.ImageField(upload_to='documents/leaving_certificate/')
    caste_certificate = models.ImageField(upload_to='documents/caste_certificate/',blank=True,null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documents - {self.application.application_number}"