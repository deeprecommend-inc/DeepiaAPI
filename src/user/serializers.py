from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserSerializerForContentList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'image')

