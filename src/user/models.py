from enum import unique
from django.db import models
from django.core.validators import RegexValidator

class User(models.Model):
    name = models.CharField(max_length=24, blank=False, null=False)
    username = models.CharField(max_length=30, blank=True, null=True, validators=[RegexValidator(r'^[a-zA-Z0-9]+$')], unique=True)
    purple = models.BooleanField(default=False)
    bio = models.TextField(max_length=80, blank=True, null=True)
    # link = models.URLField(blank=True)
    image = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
       ordering = ["-created_at"]


class UserFollowing(models.Model):
    relation_id = models.AutoField(primary_key=True, verbose_name="related-id")
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
