from django.db import models

class Content(models.Model):
    title = models.CharField(
        max_length=128, blank=False, null=False)
    deliverables = models.TextField(blank=True, null=True) # 0: imaeg, 1: music, 2: text, 3: video
    category_id = models.IntegerField(default=0, blank=False, null=False)
    user_id = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
