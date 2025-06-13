from django.db import models
from user.models import User
import json

class Content(models.Model):
    prompt = models.TextField(blank=False, null=False)
    deliverables = models.TextField(blank=True, null=True)
    category_id = models.IntegerField(default=0, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # like = models.ManyToManyField(User, related_name='related_content', blank=True)
    workflow_data = models.JSONField(blank=True, null=True)  # Workflow nodes and edges
    
    # AI Generation fields
    ai_model = models.CharField(max_length=100, blank=True, null=True)  # AI model ID (e.g., 'midjourney', 'flux_dev')
    ai_task_id = models.CharField(max_length=100, blank=True, null=True)  # PiAPI task ID
    ai_task_type = models.CharField(max_length=50, blank=True, null=True)  # Task type (e.g., 'imagine', 'generate')
    ai_parameters = models.JSONField(blank=True, null=True)  # AI generation parameters
    ai_status = models.CharField(max_length=20, default='pending', blank=True, null=True)  # pending, processing, completed, failed
    ai_result_url = models.URLField(blank=True, null=True)  # Generated content URL
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prompt
    
    class Meta:
       ordering = ["-created_at"]
