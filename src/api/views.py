from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests
import json
import logging

logger = logging.getLogger(__name__)

# PiAPI設定
PIAPI_BASE_URL = 'https://piapi.ai/api/v1'
PIAPI_KEY = 'c53e4ef1f0db3d7650c894c9dd77ed88f4a7efef37b728b2a619525c7e716fe8'

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_content(request):
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
        elif model == 'faceswap':
            endpoint = f"{PIAPI_BASE_URL}/faceswap/generate"
            payload = {
                'source_image': data.get('sourceImage'),
                'target_image': data.get('targetImage')
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
            return Response({
                'success': True,
                'data': result,
                'generation_id': result.get('id', ''),
                'status': 'processing'
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
@permission_classes([IsAuthenticated])
def check_generation_status(request, generation_id):
    """
    生成状況確認
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

@api_view(['GET'])
def get_available_models(request):
    """
    利用可能なAIモデル一覧取得
    """
    models = {
        'image': [
            {'id': 'midjourney', 'name': 'Midjourney', 'icon': '🎨'},
            {'id': 'flux', 'name': 'Flux Image', 'icon': '⚡'}
        ],
        'video': [
            {'id': 'dream_machine', 'name': 'Dream Machine', 'icon': '🎬'},
            {'id': 'kling', 'name': 'Kling Video', 'icon': '🌟'},
            {'id': 'hailuo', 'name': 'Hailuo Video', 'icon': '🌊'}
        ],
        'music': [
            {'id': 'suno', 'name': 'Suno Music', 'icon': '🎵'}
        ],
        'faceswap': [
            {'id': 'faceswap', 'name': 'FaceSwap', 'icon': '🔄'}
        ]
    }
    
    return Response({
        'success': True,
        'models': models
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_generated_content(request):
    """
    生成されたコンテンツをデータベースに保存
    """
    try:
        data = request.data
        
        # コンテンツの保存ロジック（既存のContentモデルを使用）
        # from .models import Content
        
        content_data = {
            'prompt': data.get('prompt'),
            'model_used': data.get('model'),
            'result_url': data.get('result_url'),
            'thumbnail_url': data.get('thumbnail_url'),
            'generation_id': data.get('generation_id'),
            'user': request.user,
            'category_id': data.get('category_id', 1),  # デフォルトカテゴリ
        }
        
        # 実際の保存処理（既存のContentモデルに合わせて調整）
        # content = Content.objects.create(**content_data)
        
        return Response({
            'success': True,
            'message': 'コンテンツが保存されました',
            # 'content_id': content.id
        })
        
    except Exception as e:
        logger.error(f"Save content error: {str(e)}")
        return Response(
            {'error': 'コンテンツの保存に失敗しました'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_creator_profile(request, creator_id):
    """
    クリエイタープロフィール取得
    """
    try:
        # 実際のユーザーモデルから取得
        # from django.contrib.auth.models import User
        # creator = User.objects.get(id=creator_id)
        
        # モックデータ（実際の実装では上記のコメントアウト部分を使用）
        mock_creator = {
            'id': creator_id,
            'name': 'AI Creator Pro',
            'bio': 'デジタルアートとAI生成のプロフェッショナル',
            'avatar': 'https://via.placeholder.com/80',
            'followers_count': 1250,
            'following_count': 340,
            'is_following': False,
            'specialties': ['画像生成', '動画編集', 'AI アート'],
            'created_contents_count': 85,
            'is_online': True
        }
        
        return Response({
            'success': True,
            'creator': mock_creator
        })
        
    except Exception as e:
        logger.error(f"Get creator profile error: {str(e)}")
        return Response(
            {'error': 'クリエイター情報の取得に失敗しました'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_creator(request, creator_id):
    """
    クリエイターをフォロー/アンフォロー
    """
    try:
        action = request.data.get('action', 'follow')  # follow or unfollow
        
        # 実際のフォロー機能実装
        # from .models import Follow
        # if action == 'follow':
        #     Follow.objects.get_or_create(follower=request.user, followed_id=creator_id)
        #     message = 'フォローしました'
        # else:
        #     Follow.objects.filter(follower=request.user, followed_id=creator_id).delete()
        #     message = 'フォローを解除しました'
        
        return Response({
            'success': True,
            'message': 'フォローしました' if action == 'follow' else 'フォローを解除しました',
            'is_following': action == 'follow'
        })
        
    except Exception as e:
        logger.error(f"Follow creator error: {str(e)}")
        return Response(
            {'error': 'フォロー操作に失敗しました'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )