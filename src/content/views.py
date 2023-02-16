from django.http.response import JsonResponse
from deepia_api.auth import JWTAuthentication
from content.models import Content
from content.serializers import ContentSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

def null_check(number):
    if number == None:
      return False
    return True

def has_duplicates(seq):
    return len(seq) != len(set(seq))

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def content_list(request):
    if request.method == 'GET':
        contents = Content.order_by('-created_at')
        serializer = ContentSerializer(contents, many=True)
        response = Response(serializer.data)
        return response

    if request.method == 'POST':
        new_content = {
            "title": request.data["title"],
            "deliverables": request.data["deliverables"],
            "category_id": request.data["category_id"],
            "user_id": request.user.id,
        }
        serializer = ContentSerializer(data=new_content)
        if serializer.is_valid():
            saved = serializer.save()
            content = Content.objects.get(id=saved.id)
            content.categories.set(request.data['category_ids'])
            content.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def user_content_list(request):
    if request.method == 'GET':
        contents = Content.objects.filter(user_id=request.user.id).order_by('-created_at')
        serializer = ContentSerializer(contents, many=True)
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

    # TODO: 要望次第
    # if request.method == 'PUT':
    #     new_content = {
    #         "title": request.data['title'],
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
