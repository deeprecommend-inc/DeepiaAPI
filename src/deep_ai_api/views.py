from rest_framework.permissions import IsAuthenticated
from deep_ai_api.auth import JWTAuthentication
from user.models import User
import jwt
from .settings import SECRET_KEY
import time
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.serializers import UserSerializer
from rest_framework import serializers, status
from django.contrib.auth.hashers import check_password


@api_view(['GET'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def current_user(request):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']
    try:
        user = User.objects.get(email=email)
        serializer = UserSerializer(user)
    except User.DoesNotExist:
        return Response(None)
    if not user:
        return Response(None)
    elif not check_password(password, serializer.data['password']):
        return Response(None)
    token = generate_jwt(user)
    return Response({"token": token})


def generate_jwt(user):
    timestamp = int(time.time()) + 60*60*24*7
    return jwt.encode(
        {"id": user.pk, "name": user.name,
            "email": user.email, "exp": timestamp},
        SECRET_KEY)
