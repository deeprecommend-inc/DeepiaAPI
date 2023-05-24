from django.db import models
from user.models import User

class Content(models.Model):
    prompt = models.CharField(
        max_length=128, blank=False, null=False)
    deliverables = models.TextField(blank=True, null=True)
    category_id = models.IntegerField(default=0, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='related_content', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prompt
    
    class Meta:
       ordering = ["-created_at"]