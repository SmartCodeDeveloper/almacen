from django.db import models
from .employee import Employee
from enumfields import EnumIntegerField
from enum import Enum


class TypeMov(Enum):
    INPUT    = 1
    OUTPUT   = 2
    REFUND   = 3

class Inventory(models.Model):
    employee     = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    #typemov = EnumIntegerField(TypeMov, default=TypeMov.INPUT)