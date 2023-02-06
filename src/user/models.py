from django.db import models
from log.models import Log


class User(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    image = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False, default='')

    def __str__(self):
        return self.name