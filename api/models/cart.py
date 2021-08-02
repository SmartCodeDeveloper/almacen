from django.db import models
from .employee import Employee


class Cart(models.Model):
    employee  = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)