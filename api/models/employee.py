from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    code        = models.CharField(max_length=50, null=True, blank=True)
    name        = models.CharField(max_length=50)
    lastname    = models.CharField(max_length=50)
    address     = models.TextField(null=True, blank=True)
    information = models.TextField(null=True, blank=True)
    photo       = models.ImageField(upload_to="employees", null=True, blank=True)
    active      = models.BooleanField(default=True)