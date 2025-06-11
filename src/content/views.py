from unicodedata import category
from django.http.response import JsonResponse
from api.gpt import exec_gpt
from api.gpt4 import exec_gpt4
from api.deepl import exec_deepl
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
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from user.models import User
from user.serializers import UserSerializerForContentList
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from const.content_cateogry import ContentCategory
from const.sample_datauri import sample_datauri
import requests
import json
import logging

# PiAPI設定
PIAPI_BASE_URL = 'https://piapi.ai/api/v1'
PIAPI_KEY = 'c53e4ef1f0db3d7650c894c9dd77ed88f4a7efef37b728b2a619525c7e716fe8'

logger = logging.getLogger(__name__)

def null_check(number):
    if number == None:
      return False
    return True


def has_duplicates(seq):
    return len(seq) != len(set(seq))


@api_view(['GET', 'POST'])
def content_list(request):
    if request.method == 'GET':
        search_word = request.GET.get('search_word')
        category_id = request.GET.get('category_id')
        contents_query = Content.objects.all()

        # Filtering
        if search_word and category_id:
            contents_query = contents_query.filter(Q(prompt__icontains=search_word) | Q(deliverables__icontains=search_word), category_id=category_id)
        elif search_word:
            contents_query = contents_query.filter(Q(prompt__icontains=search_word) | Q(deliverables__icontains=search_word))
        elif category_id:
            contents_query = contents_query.filter(category_id=category_id)

        # Prefetching related User objects to optimize queries
        contents = contents_query.prefetch_related('user').all()

        serializer = ContentSerializer(contents, many=True)
        
        # Map users to their IDs for faster access
        if serializer.data:
            users = {user.id: user for user in User.objects.filter(id__in=[content['user'] for content in serializer.data])}
            
            for content in serializer.data:
                user_id = content['user']
                if user_id in users:
                    user_serializer = UserSerializerForContentList(users[user_id])
                    content['user'] = user_serializer.data

        response = Response(serializer.data)
        return response
    
    elif request.method == 'POST':
        # Create new content
        title = request.data.get("title", "Untitled")
        prompt = request.data.get("prompt")
        content_type = request.data.get("content_type", "image")
        user_id = request.data.get("user_id", 1)  # フロントエンドからユーザーIDを受け取る
        
        if not prompt:
            return Response(
                {'error': 'プロンプトは必須です'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Map content_type to category_id
        category_mapping = {
            'image': ContentCategory.IMAGE.value,
            'video': ContentCategory.VIDEO.value,
            'audio': ContentCategory.MUSIC.value,
            'faceswap': ContentCategory.IMAGE.value,
        }
        
        category_id = category_mapping.get(content_type, ContentCategory.IMAGE.value)
        
        # Create content with user
        new_content = {
            "prompt": prompt,
            "deliverables": f"Generated {content_type} for: {prompt}",  # Placeholder
            "category_id": category_id,
            "user": user_id,
        }
        
        serializer = ContentSerializer(data=new_content)
        if serializer.is_valid():
            saved = serializer.save()
            
            # Return the created content with proper structure
            response_data = serializer.data
            response_data['title'] = title
            response_data['content_type'] = content_type
            response_data['likes'] = 0
            response_data['created_at'] = saved.created_at.isoformat()
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def content_create(request):
    raw_prompt = request.data.get("prompt")
    prompt = exec_deepl(raw_prompt)
    print(prompt)
    category_id = request.data.get('category_id')
    deliverables = ''
    if category_id == ContentCategory.IMAGE.value:
        deliverables = exec_stable_diffusion(prompt)
        # deliverables = sample_datauri
    elif category_id == ContentCategory.TEXT.value:
        deliverables = exec_gpt(prompt)
    elif category_id == ContentCategory.MUSIC.value:
        # TODO: Text-To-Music API
        deliverables = ''
    elif category_id == ContentCategory.VIDEO.value:
        # TODO: Text-To-Video API
        deliverables = ''
    elif category_id == ContentCategory.SPACE.value:
        # TODO: Text-To-Space API
        deliverables = ''
    else:
        category_id = ContentCategory.IMAGE.value
        deliverables = ''
    new_content = {
        "prompt": raw_prompt,
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
    # Directly filter by the user
    contents = Content.objects.filter(user=request.user)

    paginator = PageNumberPagination()
    paginated_contents = paginator.paginate_queryset(contents, request)
    serializer = ContentSerializer(paginated_contents, many=True)

    # As all the content is for the same user, just serialize the user once
    user_serializer = UserSerializerForContentList(request.user)
    user_data = user_serializer.data

    for content in serializer.data:
        content['user'] = user_data

    return Response(serializer.data)


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


@api_view(['POST'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def piapi_generate(request):
    """
    PiAPIを使用してコンテンツ生成
    """
    try:
        data = request.data
        model = data.get('model')
        prompt = data.get('prompt')
        
        if not model or not prompt:
            return Response(
                {'error': 'モデルとプロンプトは必須です'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # PiAPIリクエストの構築
        headers = {
            'X-API-Key': PIAPI_KEY,
            'Content-Type': 'application/json'
        }
        
        # モデルに応じてエンドポイントとペイロードを構築
        if model in ['midjourney', 'flux']:
            endpoint = f"{PIAPI_BASE_URL}/midjourney/generate"
            payload = {
                'prompt': prompt,
                'aspect_ratio': data.get('aspectRatio', '16:9'),
                'process_mode': 'fast',
                'webhook_endpoint': '',
                'webhook_secret': ''
            }
        elif model in ['dream_machine', 'kling', 'hailuo']:
            endpoint = f"{PIAPI_BASE_URL}/dream-machine/generate"
            payload = {
                'prompt': prompt,
                'duration': data.get('duration', '10s'),
                'quality': data.get('resolution', '1080p'),
                'aspect_ratio': data.get('aspectRatio', '16:9')
            }
        elif model == 'suno':
            endpoint = f"{PIAPI_BASE_URL}/suno/generate"
            payload = {
                'custom_mode': False,
                'input': {
                    'prompt': prompt,
                    'make_instrumental': data.get('instrumental', False)
                }
            }
        else:
            return Response(
                {'error': f'サポートされていないモデル: {model}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"PiAPI request - Model: {model}, Endpoint: {endpoint}")
        
        # PiAPIへのリクエスト送信
        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # コンテンツをデータベースに保存
            category_id = ContentCategory.IMAGE.value
            if model in ['dream_machine', 'kling', 'hailuo']:
                category_id = ContentCategory.VIDEO.value
            elif model == 'suno':
                category_id = ContentCategory.MUSIC.value
                
            new_content = {
                "prompt": prompt,
                "deliverables": result.get('result', {}).get('url', ''),
                "category_id": category_id,
                "user": request.user.id,
            }
            
            serializer = ContentSerializer(data=new_content)
            if serializer.is_valid():
                saved = serializer.save()
                
            return Response({
                'success': True,
                'data': result,
                'generation_id': result.get('id', ''),
                'status': 'processing',
                'content_id': saved.id if 'saved' in locals() else None
            })
        else:
            logger.error(f"PiAPI error: {response.status_code} - {response.text}")
            return Response(
                {'error': 'PiAPI呼び出しに失敗しました', 'details': response.text},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except requests.RequestException as e:
        logger.error(f"Network error: {str(e)}")
        return Response(
            {'error': 'ネットワークエラーが発生しました'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response(
            {'error': 'サーバーエラーが発生しました'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def piapi_status(request, generation_id):
    """
    PiAPI生成状況確認
    """
    try:
        headers = {
            'X-API-Key': PIAPI_KEY,
            'Content-Type': 'application/json'
        }
        
        endpoint = f"{PIAPI_BASE_URL}/status/{generation_id}"
        response = requests.get(endpoint, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return Response({
                'success': True,
                'data': result
            })
        else:
            return Response(
                {'error': '状況確認に失敗しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        return Response(
            {'error': 'サーバーエラーが発生しました'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
