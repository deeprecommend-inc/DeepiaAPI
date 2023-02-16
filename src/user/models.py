from enum import unique
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    bio = models.TextField(max_length=80, blank=True, null=True)
    # userid = models.CharField(unique=True, blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False, default='')

    def __str__(self):
        return self.name
