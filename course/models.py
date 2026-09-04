from django.db import models

class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=20, unique=True)

    department = models.CharField(max_length=50)
    duration = models.IntegerField(help_text="Duration In Years")

    total_seats = models.IntegerField(default=0)
    available_seats = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course_name}, {self.course_code}"