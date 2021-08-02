from django.db import models

class Unit(models.Model):
    name   = models.CharField(max_length=30)
    active = models.BooleanField(default=True)