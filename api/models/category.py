from django.db import models


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    code   = models.CharField(max_length=100)
    name   = models.CharField(max_length=100)
    active = models.BooleanField(default=True)