from category.models import Category
from category.serializers import CategorySerializer
from deep_ai_api.auth import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from log.models import Log
from log.serializers import LogSerializer


@api_view(['GET'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def category_log_list(request, pk):
    if request.method == 'GET':
        category = Category.objects.get(pk=pk)
        category_logs = category.log_set.all().order_by('-index')
        serializer = LogSerializer(category_logs, many=True)
        response = Response(serializer.data)
        return response


@api_view(['POST', 'PUT'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def update_categories(request):
    if request.method == 'POST':
        for id in request.data['log_ids']:
            log = Log.objects.get(id=id)
            log.categories.set(request.data['category_ids'])
            log.save()
        return Response(status.HTTP_204_NO_CONTENT)
    
    if request.method == 'PUT':
        log = Log.objects.get(id=request.data['log_id'])
        log.categories.set(request.data['category_ids'])
        log.save()
        return Response(status=status.HTTP_201_CREATED)
