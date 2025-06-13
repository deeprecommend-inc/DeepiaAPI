from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from deepia_api.auth import JWTAuthentication
from .models import Comment, Like
from .serializers import CommentSerializer, LikeSerializer, FollowSerializer
from content.models import Content
from user.models import User, UserFollowing
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def content_comments(request, content_id):
    """
    コンテンツのコメント一覧取得・コメント投稿
    """
    content = get_object_or_404(Content, id=content_id)
    
    if request.method == 'GET':
        comments = Comment.objects.filter(content=content, parent=None)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        text = request.data.get('text', '').strip()
        parent_id = request.data.get('parent_id')
        
        if not text:
            return Response(
                {'error': 'コメント内容を入力してください'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id, content=content)
        
        comment = Comment.objects.create(
            content=content,
            user=request.user,
            text=text,
            parent=parent
        )
        
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_id):
    """
    コメント詳細取得・編集・削除
    """
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'GET':
        # 返信も含めて取得
        replies = Comment.objects.filter(parent=comment)
        comment_data = CommentSerializer(comment, context={'request': request}).data
        replies_data = CommentSerializer(replies, many=True, context={'request': request}).data
        comment_data['replies'] = replies_data
        return Response(comment_data)
    
    elif request.method == 'PUT':
        if comment.user != request.user:
            return Response(
                {'error': 'このコメントを編集する権限がありません'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        text = request.data.get('text', '').strip()
        if not text:
            return Response(
                {'error': 'コメント内容を入力してください'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comment.text = text
        comment.save()
        
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if comment.user != request.user:
            return Response(
                {'error': 'このコメントを削除する権限がありません'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def toggle_like(request):
    """
    いいね・いいね解除
    """
    content_id = request.data.get('content_id')
    comment_id = request.data.get('comment_id')
    
    if not content_id and not comment_id:
        return Response(
            {'error': 'content_id または comment_id が必要です'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if content_id and comment_id:
        return Response(
            {'error': 'content_id と comment_id は同時に指定できません'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if content_id:
        content = get_object_or_404(Content, id=content_id)
        like, created = Like.objects.get_or_create(
            user=request.user,
            content=content,
            defaults={'content': content}
        )
    else:
        comment = get_object_or_404(Comment, id=comment_id)
        like, created = Like.objects.get_or_create(
            user=request.user,
            comment=comment,
            defaults={'comment': comment}
        )
    
    if request.method == 'POST':
        if not created:
            return Response(
                {'message': '既にいいねしています', 'liked': True},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'いいねしました', 'liked': True},
            status=status.HTTP_201_CREATED
        )
    
    elif request.method == 'DELETE':
        like.delete()
        return Response(
            {'message': 'いいねを取り消しました', 'liked': False},
            status=status.HTTP_200_OK
        )


@api_view(['POST', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def toggle_follow(request, user_id):
    """
    フォロー・アンフォロー
    """
    target_user = get_object_or_404(User, id=user_id)
    
    if target_user == request.user:
        return Response(
            {'error': '自分自身をフォローすることはできません'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    follow, created = UserFollowing.objects.get_or_create(
        user_id=request.user,
        following_user_id=target_user
    )
    
    if request.method == 'POST':
        if not created:
            return Response(
                {'message': '既にフォローしています', 'following': True},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'フォローしました', 'following': True},
            status=status.HTTP_201_CREATED
        )
    
    elif request.method == 'DELETE':
        follow.delete()
        return Response(
            {'message': 'フォローを解除しました', 'following': False},
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_followers(request, user_id):
    """
    ユーザーのフォロワー一覧
    """
    user = get_object_or_404(User, id=user_id)
    followers = UserFollowing.objects.filter(following_user_id=user)
    serializer = FollowSerializer(followers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_following(request, user_id):
    """
    ユーザーのフォロー中一覧
    """
    user = get_object_or_404(User, id=user_id)
    following = UserFollowing.objects.filter(user_id=user)
    serializer = FollowSerializer(following, many=True)
    return Response(serializer.data)