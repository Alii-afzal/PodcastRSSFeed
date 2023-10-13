import jwt
import datetime
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework import permissions

from .authentication import JWTAuthentication
from accounts.models import User
from .utils import create_jti, create_access_token, create_refresh_token, cache_key_setter, cache_value_setter, decode_jwt, delete_cache, cache_refresh_token, validate_cached_token
from accounts.serializers import UserRegisterSerializer, UserLoginSerializer

from .authbackend import AuthenticationBackend

from config import settings
  
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        auth = AuthenticationBackend()
        user = auth.authenticate(request, email=email, password=password)
        # print(user)
        # print(request.data)
        # print(email)
        # print(password)
        # print(serializer.errors)
        if user is None:
            return Response(data={'message': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        jti = create_jti()
        access_token = create_access_token(user.id, jti)
        refresh_token = create_refresh_token(user.id, jti)
        
        # key = cache_key_setter(user.id, jti)
        # value = cache_value_setter(request)
        # refresh_expired_time = settings.REFRESH_EXPIRED_TIME
        # cache.set(key=key, value=value, timeout=refresh_expired_time)
        cache_refresh_token(decode_jwt(refresh_token))
        
        data = {
            "access": access_token,
            "refresh": refresh_token 
        }
        
        return Response(data=data, status=status.HTTP_201_CREATED)



class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        refresh_token = decode_jwt(refresh_token)
        
        if not validate_cached_token(refresh_token):
            return Response(data={"message":"Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = refresh_token.get('user_id')
        jti = refresh_token.get('jti')
        
        access_token = create_access_token(user_id, jti)
        refresh_token = create_refresh_token(user_id, jti)
        
        # key = cache_key_setter(user_id, jti)
        # value = cache_value_setter(request)
 
        delete_cache(jti)
        # cache.set(key=key, value=value, timeout=refresh_expired_time)
        cache_refresh_token(decode_jwt(refresh_token))
        
        data = {
            "access" : access_token, 
            "refresh" : refresh_token,
        }
        
        return Response(data=data, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        jti = decode_jwt(access_token).get('jti')
        delete_cache(jti)
        return Response(status=status.HTTP_204_NO_CONTENT)


# class LogoutAPIView(APIView):
#     def post(self, request):
#         try:
#             payload = request.auth
#             user = request.user
#             jti = payload["jti"]
#             caches['auth'].delete(f"user_{user.id} || {jti}")
            
#             return Response(data={"message":True}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(data={"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AuthenticatedView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )

    def get(self, request):
        return Response(data={"message": "you are authenticated"}, status=status.HTTP_200_OK)