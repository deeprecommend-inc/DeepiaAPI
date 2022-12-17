from django.db.models import fields
from rest_framework import serializers
from log.models import Log
from category.serializers import CategorySerializer


class LogSerializer(serializers.ModelSerializer):
    # categories = CategorySerializer(many=True)
    
    class Meta:
        model = Log
        fields = '__all__'
