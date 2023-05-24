from unicodedata import category
from django.http.response import JsonResponse
from api.gpt import exec_gpt
from deepia_api.auth import JWTAuthentication
from content.models import Content
from content.serializers import ContentSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from PIL import Image
import os
from api.stable_diffusion import exec_stable_diffusion
from api.gpt import exec_gpt
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from user.models import User
from user.serializers import UserSerializerForContentList
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from const.content_cateogry import ContentCategory

def null_check(number):
    if number == None:
      return False
    return True

def has_duplicates(seq):
    return len(seq) != len(set(seq))

@api_view(['GET'])
def content_list(request):
    search_word = request.GET.get('search_word')
    category_id = request.GET.get('category_id')
    if not search_word and not category_id:
        contents = Content.objects.all()
    elif not category_id:
        contents = Content.objects.filter(Q(title__icontains=search_word) | Q(description__icontains=search_word)).all()
    elif not search_word:
        contents = Content.objects.filter(category_id=category_id).all()
    else:
        contents = Content.objects.filter(category_id=category_id).filter(Q(title__icontains=search_word) | Q(description__icontains=search_word)).all()
    paginator = PageNumberPagination()
    paginated_contents = paginator.paginate_queryset(contents, request)
    serializer = ContentSerializer(paginated_contents, many=True)
    user_ids = [content.user_id for content in contents]
    users = User.objects.filter(id__in=user_ids)
    user_serializer = UserSerializerForContentList(users, many=True)
    for content in serializer.data:
        user_id = content['user']
        index = user_ids.index(user_id)
        if index < len(user_serializer.data):
            new_user = user_serializer.data[index]
            content['user'] = new_user
    response = Response(serializer.data)
    return response


@api_view(['POST'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def content_create(request):
    prompt = request.data["prompt"]
    category_id = request.data['category_id']
    deliverables = ''
    if category_id == ContentCategory.IMAGE:
        deliverables = exec_stable_diffusion(prompt)
    elif category_id == ContentCategory.TEXT:
        deliverables = exec_gpt(prompt)
    elif category_id == ContentCategory.MUSIC:
    # TODO: Text-To-Music API
        return
    elif category_id == ContentCategory.VIDEO:
        # TODO: Text-To-Video API
        return
    elif category_id == ContentCategory.SPACE:
        # TODO: Text-To-Space API
        return
    else:
        return
    new_content = {
        "prompt": prompt,
        "deliverables": deliverables,
        "category_id": category_id,
        "user": request.user.id,
    }
    serializer = ContentSerializer(data=new_content)
    if serializer.is_valid():
        saved = serializer.save()
        content = Content.objects.get(id=saved.id)
        content.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def user_content_list(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        if category_id == None:
            contents = Content.objects.filter(user_id=request.user.id).order_by('-created_at')
        else:
            contents = Content.objects.filter(user_id=request.user.id, category_id=category_id).order_by('-created_at')
        paginator = PageNumberPagination()
        paginated_contents = paginator.paginate_queryset(contents, request)
        serializer = ContentSerializer(paginated_contents, many=True)
        user_ids = [content.user_id for content in contents]
        users = User.objects.filter(id__in=user_ids)
        user_serializer = UserSerializerForContentList(users, many=True)
        for content in serializer.data:
            content_user_id = content['user']
            content['user'] = user_serializer.data[user_ids.index(content_user_id)]
        response = Response(serializer.data)
        return response


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def content_detail(request, pk):
    try:
        content = Content.objects.get(pk=pk)
    except Content.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContentSerializer(content)
        return Response(serializer.data)
    
    # if request.method == 'PUT':
    #     new_content = {
    #         "prompt": request.data['prompt'],
    #         "user_id": request.user.id,
    #     }
    #     serializer = ContentSerializer(content, data=new_content)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
