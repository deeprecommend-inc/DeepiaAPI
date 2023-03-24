from django.db.models import fields
from rest_framework import serializers
from content.models import Content
from user.serializers import UserSerializerForContentList


class ContentSerializer(serializers.ModelSerializer):
    user = UserSerializerForContentList()
    
    class Meta:
        model = Content
        fields = '__all__'
