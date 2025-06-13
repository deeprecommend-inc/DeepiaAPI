from rest_framework import serializers
from .models import Comment, Like
from user.models import UserFollowing
from user.serializers import UserSerializerForContentList

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializerForContentList(read_only=True)
    replies_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'parent', 'created_at', 'updated_at', 
                 'replies_count', 'likes_count', 'is_liked']
    
    def get_replies_count(self, obj):
        return obj.replies.count()
    
    def get_likes_count(self, obj):
        return Like.objects.filter(comment=obj).count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, comment=obj).exists()
        return False


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'created_at']


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializerForContentList(source='user_id', read_only=True)
    following = UserSerializerForContentList(source='following_user_id', read_only=True)
    
    class Meta:
        model = UserFollowing
        fields = ['relation_id', 'follower', 'following', 'created']