from rest_framework import serializers
from user.models import User, UserFollowing

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ("relation_id", "following_user_id", "created")


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ("relation_id", "user_id", "created")


class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'purple', 'bio', 'image',
                'email', 'password', 'following', "followers")

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data


class UserSerializerForContentList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'image')


class UserSerializerForAdminApi(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'purple', 'email')
