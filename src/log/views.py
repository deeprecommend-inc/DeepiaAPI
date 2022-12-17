from django.http.response import JsonResponse
from category.views import has_duplicates
from deep_ai_api.auth import JWTAuthentication
from log.models import Log
from log.serializers import LogSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from category.models import Category

def null_check(number):
    if number == None:
      return False
    return True

def has_duplicates(seq):
    return len(seq) != len(set(seq))

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def log_list(request):
    if request.method == 'GET':
        logs = Log.objects.filter(user_id=request.user.id)
        for i, log in enumerate(logs):
            log_indices = Log.objects.filter(user_id=request.user.id).values_list('index', flat=True)
            if log.index == None or has_duplicates(log_indices):
                new_log = {
                    "title": log.title,
                    "memo": log.memo,
                    "link": log.link,
                    "user_id": log.user_id,
                    "index": 0 if i == 0 else max(filter(null_check, log_indices)) + 1,
                }
                serializer = LogSerializer(log, data=new_log)
                if serializer.is_valid():
                    serializer.save()
        
        logs_have_index = Log.objects.filter(user_id=request.user.id).order_by('-index')
        serializer = LogSerializer(logs_have_index, many=True)
        response = Response(serializer.data)
        return response

    if request.method == 'POST':
        log_indices = Log.objects.filter(user_id=request.user.id).values_list('index', flat=True)

        new_log = {
            "title": request.data["title"],
            "memo": request.data["memo"],
            "link": request.data["link"],
            "user_id": request.user.id,
            "index": 0 if len(log_indices) == 0 else max(filter(null_check, log_indices)) + 1,
        }
        serializer = LogSerializer(data=new_log)
        if serializer.is_valid():
            saved = serializer.save()
            log = Log.objects.get(id=saved.id)
            log.categories.set(request.data['category_ids'])
            log.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def log_detail(request, pk):
    try:
        log = Log.objects.get(pk=pk)
    except Log.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LogSerializer(log)
        return Response(serializer.data)

    if request.method == 'PUT':
        new_log = {
            "title": request.data['title'],
            "memo": request.data['memo'],
            "link": request.data["link"],
            "user_id": request.user.id,
            "index": log.index,
        }
        serializer = LogSerializer(log, data=new_log)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def log_remover(request):
    for id in request.data['ids']:
        log = get_object_or_404(Log, id=id)
        log.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def log_drag_and_drop(request):
    if request.method == 'PUT':
        source = Log.objects.get(id=request.data["source_id"])
        target = Log.objects.get(id=request.data["target_id"])
        update_source = Log.objects.get(id=request.data["source_id"])
        update_target = Log.objects.get(id=request.data["target_id"])
        category_id =  request.data["category_id"]
        
        update_source.index = target.index
        update_target.index = source.index

        update_source.save()
        update_target.save()

        if category_id == None:
            logs = Log.objects.filter(user_id=request.user.id)
            for i, log in enumerate(logs):
                log_indices = Log.objects.filter(user_id=request.user.id).values_list('index', flat=True)
                if log.index == None or has_duplicates(log_indices):
                    new_log = {
                        "title": log.title,
                        "memo": log.memo,
                        "link": log.link,
                        "user_id": log.user_id,
                        "index": 0 if i == 0 else max(filter(null_check, log_indices)) + 1,
                    }
                    serializer = LogSerializer(log, data=new_log)
                    if serializer.is_valid():
                        serializer.save()

            logs_have_index = Log.objects.filter(user_id=request.user.id).order_by('-index')
            serializer = LogSerializer(logs_have_index, many=True)
            response = Response(serializer.data)
            return response
        else:
            category = Category.objects.get(id=category_id)
            category_logs = category.log_set.all().order_by('-index')
            serializer = LogSerializer(category_logs, many=True)
            response = Response(serializer.data)
            return response