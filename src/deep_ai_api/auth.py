import time
from rest_framework import exceptions, status
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.response import Response

from user.serializers import UserSerializer
from .settings import SECRET_KEY
import jwt
from user.models import User


class JWTAuthentication(BaseAuthentication):
    keyword = 'Bearer'
    model = None

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            raise Response(status=status.HTTP_400_BAD_REQUEST)
        elif len(auth) > 2:
            raise Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            jwt_token = auth[1]
            jwt_info = jwt.decode(jwt_token, SECRET_KEY)
            user_id = jwt_info.get("id")
            try:
                user = User.objects.get(pk=user_id)
                user.is_authenticated = True
                return (user, jwt_token)
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

    def authenticate_header(self, request):
        pass
