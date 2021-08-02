from django.db import models


class Notification(models.Model):
    message      = models.TextField()
    read         = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)