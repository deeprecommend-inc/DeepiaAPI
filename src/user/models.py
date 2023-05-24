from enum import unique
from django.db import models
from django.core.validators import RegexValidator

class User(models.Model):
    name = models.CharField(max_length=24, blank=False, null=False)
    username = models.CharField(max_length=30, blank=True, null=True, validators=[RegexValidator(r'^[a-zA-Z0-9]+$')])
    purple = models.BooleanField(default=False)
    bio = models.TextField(max_length=80, blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    following = models.ManyToManyField("self", related_name="followed_by", symmetrical=False,blank=True)
    password = models.CharField(max_length=128, blank=False, null=False, default='')

    def __str__(self):
        return self.name
