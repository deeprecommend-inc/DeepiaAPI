from django.http.response import JsonResponse
from category.views import has_duplicates
from deepia_api.auth import JWTAuthentication
from content.models import Content
from content.serializers import ContentSerializer
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
def content_list(request):
    if request.method == 'GET':
        contents = Content.objects.filter(user_id=request.user.id)
        for i, content in enumerate(contents):
            content_indices = Content.objects.filter(user_id=request.user.id).values_list('index', flat=True)
            if content.index == None or has_duplicates(content_indices):
                new_content = {
                    "title": content.title,
                    "memo": content.memo,
                    "link": content.link,
                    "user_id": content.user_id,
                    "index": 0 if i == 0 else max(filter(null_check, content_indices)) + 1,
                }
                serializer = ContentSerializer(content, data=new_content)
                if serializer.is_valid():
                    serializer.save()
        
        contents_have_index = Content.objects.filter(user_id=request.user.id).order_by('-index')
        serializer = ContentSerializer(contents_have_index, many=True)
        response = Response(serializer.data)
        return response

    if request.method == 'POST':
        content_indices = Content.objects.filter(user_id=request.user.id).values_list('index', flat=True)

        new_content = {
            "title": request.data["title"],
            "memo": request.data["memo"],
            "link": request.data["link"],
            "user_id": request.user.id,
            "index": 0 if len(content_indices) == 0 else max(filter(null_check, content_indices)) + 1,
        }
        serializer = ContentSerializer(data=new_content)
        if serializer.is_valid():
            saved = serializer.save()
            content = Content.objects.get(id=saved.id)
            content.categories.set(request.data['category_ids'])
            content.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
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

    if request.method == 'PUT':
        new_content = {
            "title": request.data['title'],
            "memo": request.data['memo'],
            "link": request.data["link"],
            "user_id": request.user.id,
            "index": content.index,
        }
        serializer = ContentSerializer(content, data=new_content)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def content_remover(request):
    for id in request.data['ids']:
        content = get_object_or_404(Content, id=id)
        content.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['PUT'])
# @authentication_classes([JWTAuthentication, ])
# @permission_classes([IsAuthenticated, ])
# def content_drag_and_drop(request):
#     if request.method == 'PUT':
#         source = Content.objects.get(id=request.data["source_id"])
#         target = Content.objects.get(id=request.data["target_id"])
#         update_source = Content.objects.get(id=request.data["source_id"])
#         update_target = Content.objects.get(id=request.data["target_id"])
#         category_id =  request.data["category_id"]
        
#         update_source.index = target.index
#         update_target.index = source.index

#         update_source.save()
#         update_target.save()

#         if category_id == None:
#             contents = Content.objects.filter(user_id=request.user.id)
#             for i, content in enumerate(contents):
#                 content_indices = Content.objects.filter(user_id=request.user.id).values_list('index', flat=True)
#                 if content.index == None or has_duplicates(content_indices):
#                     new_content = {
#                         "title": content.title,
#                         "memo": content.memo,
#                         "link": content.link,
#                         "user_id": content.user_id,
#                         "index": 0 if i == 0 else max(filter(null_check, content_indices)) + 1,
#                     }
#                     serializer = ContentSerializer(content, data=new_content)
#                     if serializer.is_valid():
#                         serializer.save()

#             contents_have_index = Content.objects.filter(user_id=request.user.id).order_by('-index')
#             serializer = ContentSerializer(contents_have_index, many=True)
#             response = Response(serializer.data)
#             return response
#         else:
#             category = Category.objects.get(id=category_id)
#             category_contents = category.content_set.all().order_by('-index')
#             serializer = ContentSerializer(category_contents, many=True)
#             response = Response(serializer.data)
#             return response