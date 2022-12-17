from django.http.response import JsonResponse
from category.models import Category
from category.serializers import CategorySerializer
from deep_ai_api.auth import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
from user.models import User
from user.serializers import UserSerializer


def null_check(number):
    if number == None:
      return False
    return True

def has_duplicates(seq):
    return len(seq) != len(set(seq))


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.filter(user_id=request.user.id)
        for i, category in enumerate(categories):
            category_indices = Category.objects.filter(user_id=request.user.id).values_list('index', flat=True)
            if category.index == None or has_duplicates(category_indices):
                new_category = {
                    "name": category.name,
                    "user_id": category.user_id,
                    "index": 0 if i == 0 else max(filter(null_check, category_indices)) + 1,
                    "image": category.image,
                    "public": category.public
                }
                serializer = CategorySerializer(category, data=new_category)
                if serializer.is_valid():
                    serializer.save()
        
        categories_have_index = Category.objects.filter(user_id=request.user.id).order_by('index')
        serializer = CategorySerializer(categories_have_index, many=True)
        response = Response(serializer.data)
        return response

    if request.method == 'POST':
        category_indices = Category.objects.filter(user_id=request.user.id).values_list('index', flat=True)
        
        def get_image():
            try:
                return request.data["image"]
            except:
                return ''
        
        new_category = {
            "name": request.data["name"],
            "user_id": request.user.id,
            "index": 0 if len(category_indices) == 0 else max(filter(null_check, category_indices)) + 1,
            "image": get_image(),
            "public": request.data["public"]
        }
        serializer = CategorySerializer(data=new_category)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def public_category_list(request):
    if request.method == 'GET':
        new_categories = []
        categories = Category.objects.exclude(user_id=request.user.id).filter(public=True).order_by('-created_at')
        for i, category in enumerate(categories):
            user = User.objects.get(id=category.user_id)
            new_category = {
                "id": category.id,
                "name": category.name,
                "index": category.index,
                "image": category.image,
                "public": category.public,
                "user_id": category.user_id,
                "user_icon": user.image,
                "user_name": user.name,
                "created_at": category.created_at
            }
            new_categories.append(new_category)
        response = Response(new_categories)
        print(new_categories)
        return response


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    if request.method == 'PUT':
        def get_image():
            try:
                return request.data["image"]
            except:
                return category.image
        
        new_category = {
            "name": request.data["name"],
            "user_id": request.user.id,
            "index": category.index,
            "image": get_image(),
            "public": request.data["public"]
        }
        serializer = CategorySerializer(category, data=new_category)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def category_drag_and_drop(request):
    if request.method == 'PUT':
        source = Category.objects.get(id=request.data["source_id"])
        target = Category.objects.get(id=request.data["target_id"])
        update_source = Category.objects.get(id=request.data["source_id"])
        update_target = Category.objects.get(id=request.data["target_id"])

        update_source.index = target.index
        update_target.index = source.index

        update_source.save()
        update_target.save()

        categories = Category.objects.filter(user_id=request.user.id)
        for i, category in enumerate(categories):
            category_indices = Category.objects.filter(user_id=request.user.id).values_list('index', flat=True)
            if category.index == None or has_duplicates(category_indices):
                new_category = {
                    "name": category.name,
                    "user_id": category.user_id,
                    "index": 0 if i == 0 else max(filter(null_check, category_indices)) + 1,
                    "image": category.image,
                    "public": category.public,
                }
                serializer = CategorySerializer(category, data=new_category)
                if serializer.is_valid():
                    serializer.save()
        
        categories_have_index = Category.objects.filter(user_id=request.user.id).order_by('index')
        serializer = CategorySerializer(categories_have_index, many=True)
        response = Response(serializer.data)
        return response

