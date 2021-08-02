from django.db import models
from .employee import Employee
from enumfields import EnumIntegerField
from enum import Enum

class Priority(Enum):
    LOW    = 1
    MEDIUM = 2
    HIGH   = 3

class OrderStatus(Enum):
    PENDING  = 1
    APPROVED = 2
    DENIED   = 3
    

class Order(models.Model):
    employee  = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    priority  = models.IntegerField(default=1)
    status    = models.IntegerField(default=1)
    torder    = models.IntegerField(default=1)
    tpayment  = models.IntegerField(default=1)
    active    = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    date_delivery = models.DateField(null=True, blank=True)
    date_delivery2 = models.DateField(null=True, blank=True)
    hour_delivery  = models.TimeField(null=True, blank=True)
    date_created  = models.DateTimeField(auto_now_add=True)
    date_updated  = models.DateTimeField(auto_now=True)