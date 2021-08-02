from django.db import models
from .employee import Employee

class Movement(models.Model):
    fromemployee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL, related_name="movfromemployees")
    toemployee   = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL, related_name="movtoemployees")
    client       = models.CharField(max_length=100, null=True, blank=True)
    sign         = models.ImageField(upload_to="signs", null=True, blank=True)
    typemov      = models.IntegerField()
    observations = models.TextField(null=True, blank=True)
    datemov      = models.DateTimeField(auto_now_add=True)
    status       = models.IntegerField(default=1)