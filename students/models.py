from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):

    Gender_choice = (
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other'),
    )

    CategoryChoice = (
        ('General','General'),
        ('OBC', 'OBD'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('EWS', 'EWS'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=Gender_choice, max_length=10)
    category = models.CharField(choices=CategoryChoice, max_length=10)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username
