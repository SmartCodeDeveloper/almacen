from django.db import models

class Brand(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    photo       = models.ImageField(upload_to='brands', null=True, blank=True)
    active      = models.BooleanField(default=True)