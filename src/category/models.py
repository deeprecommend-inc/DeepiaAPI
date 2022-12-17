from email.policy import default
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    index = models.IntegerField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    public = models.BooleanField(verbose_name='', default=False)
    user_id = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
