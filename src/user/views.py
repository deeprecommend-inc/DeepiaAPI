from deepia_api.auth import JWTAuthentication
from user.models import User, UserFollowing
from user.serializers import UserSerializer, UserSerializerForAdminApi, FollowingSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        new_user = {
            "name": request.data["name"],
            "username": request.data["name"],
            "email": request.data["email"],
            "password": make_password(request.data["password"])
        }
        serializer = UserSerializer(data=new_user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def is_unique_email(request):
    is_unique_email = User.objects.filter(email=request.data['email']).exists()
    return Response(not is_unique_email)


@api_view(['POST'])
def is_unique_username(request):
    is_unique_username = User.objects.filter(email=request.data['username']).exists()
    return Response(not is_unique_username)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_purple_update(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        user.purple = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    if request.method == 'DELETE':
        user.purple = False
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_list_for_admin(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializerForAdminApi(users, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def follow_user(request):
    serializer = FollowingSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(id=request.data['user_id'])
        following_user = User.objects.get(id=request.data['following_user_id'])

        if user == following_user:
            return Response({"detail": "Cannot follow yourself"}, status=400)

        relation, created = UserFollowing.objects.get_or_create(user_id=user, following_user_id=following_user)

        if created:
            return Response({"detail": "User followed"}, status=201)
        else:
            return Response({"detail": "Already following"}, status=400)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def unfollow_user(request, following_user_id):
    relation = UserFollowing.objects.filter(user_id=request.user.id, following_user_id=following_user_id)

    if relation.exists():
        relation.delete()
        return Response({"detail": "User unfollowed"}, status=200)

    return Response({"detail": "You are not following this user"}, status=400)
