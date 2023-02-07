from django.db.models import fields
from rest_framework import serializers
from content.models import Content
from category.serializers import CategorySerializer


class ContentSerializer(serializers.ModelSerializer):
    # categories = CategorySerializer(many=True)
    
    class Meta:
        model = Content
        fields = '__all__'
