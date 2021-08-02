from django.db import models
from .employee import Employee
from .order    import Order


class Manifest(models.Model):
    order         = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    employee      = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    receive       = models.CharField(max_length=60, null=True, blank=True)
    delivery      = models.CharField(max_length=60, null=True, blank=True)
    active        = models.BooleanField(default=True)
    printer       = models.BooleanField(default=False)
    description   = models.TextField(null=True, blank=True)
    date_manifest = models.DateField(null=True, blank=True)