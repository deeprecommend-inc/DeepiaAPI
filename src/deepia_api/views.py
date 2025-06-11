from rest_framework.permissions import IsAuthenticated
from deepia_api.auth import JWTAuthentication
from user.models import User
import jwt
from .settings import SECRET_KEY
import time
import uuid
import hashlib
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.serializers import UserSerializer
from rest_framework import serializers, status
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.conf import settings


@api_view(['GET'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def current_user(request):
    try:
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
    except User.DoesNotExist:
        return Response(None)
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


@api_view(['POST'])
def register(request):
    """
    ユーザー登録とメール認証
    """
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not all([name, email, password]):
            return Response(
                {'error': '全ての項目を入力してください'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # メールアドレスの重複チェック
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'このメールアドレスは既に登録されています'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 認証トークンを生成
        verification_token = str(uuid.uuid4())
        
        # ユーザーを作成（未認証状態）
        user = User.objects.create(
            name=name,
            email=email,
            password=make_password(password),
            username=email.split('@')[0],  # メールの@より前をユーザー名として使用
            # 認証トークンを保存する場合（カスタムフィールドが必要）
        )
        
        # メール認証リンクを送信（開発環境では簡略化）
        verification_url = f"http://localhost:3001/verify?token={verification_token}&user_id={user.id}"
        
        # 開発環境では実際のメール送信は行わず、ログに出力
        print(f"認証URL: {verification_url}")
        
        return Response({
            'message': 'ユーザー登録が完了しました。メールを確認して認証を完了してください。',
            'verification_url': verification_url,  # 開発用
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'登録に失敗しました: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def verify_email(request, token):
    """
    メール認証（簡略版）
    """
    user_id = request.GET.get('user_id')
    
    if not user_id:
        return Response(
            {'error': '無効な認証リンクです'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
        # 認証完了（実際のプロダクションではトークンの検証が必要）
        
        # JWTトークンを生成してログイン状態にする
        jwt_token = generate_jwt(user)
        
        return Response({
            'message': 'メール認証が完了しました',
            'token': jwt_token,
            'user': UserSerializer(user).data
        })
        
    except User.DoesNotExist:
        return Response(
            {'error': 'ユーザーが見つかりません'},
            status=status.HTTP_404_NOT_FOUND
        )


def generate_jwt(user):
    timestamp = int(time.time()) + 60*60*24*7
    return jwt.encode(
        {"id": user.pk, "name": user.name,
            "email": user.email, "exp": timestamp},
        SECRET_KEY)
