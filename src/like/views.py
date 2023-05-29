
from unicodedata import category
from django.http.response import JsonResponse
from deepia_api.auth import JWTAuthentication
from content.models import Content
from content.serializers import ContentSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def like_list(request):
    return

@api_view(['GET'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def like_detail(request):
    return