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
from .utils import create_jti, create_access_token, create_refresh_token, decode_jwt, delete_cache, cache_refresh_token, validate_cached_token
from accounts.serializers import UserRegisterSerializer, UserLoginSerializer

from .authbackend import AuthenticationBackend
from .publisher import Publish

from config import settings
  
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        
        request_META = request.META.get('HTTP_USER_AGENT')
        email = request.data.get('email')
        Publish().register(email=email, request_META=request_META)
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
        if user is None:
            return Response(data={'message': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        jti = create_jti()
        access_token = create_access_token(user.id, jti)
        refresh_token = create_refresh_token(user.id, jti)
        
        cache_refresh_token(decode_jwt(refresh_token))
        
        data = {
            "access": access_token,
            "refresh": refresh_token 
        }
        
        request_META = request.META.get('HTTP_USER_AGENT')
        Publish().login(email=email, request_META=request_META)
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
        

 
        delete_cache(jti)
        cache_refresh_token(decode_jwt(refresh_token))
        
        data = {
            "access" : access_token, 
            "refresh" : refresh_token,
        }
        
        return Response(data=data, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        jti = decode_jwt(refresh_token).get('jti')
        delete_cache(jti)
        message = {'status' : 'Logout done successfully.'}
        return Response(message , status=status.HTTP_204_NO_CONTENT)