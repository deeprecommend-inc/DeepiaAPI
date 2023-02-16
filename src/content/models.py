from django.db import models

class Content(models.Model):
    title = models.CharField(
        max_length=128, blank=False, null=False)
    deliverables = models.TextField(blank=True, null=True)
    category_id = models.IntegerField(blank=False, null=False)
    user_id = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
