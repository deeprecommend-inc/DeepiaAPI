from django.db import models
from category.models import Category

class Log(models.Model):
    title = models.CharField(
        max_length=128, blank=False, null=False)
    memo = models.CharField(
        max_length=512, blank=True, null=True)
    link = models.URLField(
        max_length=512, blank=False, null=False)
    index = models.IntegerField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    user_id = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
