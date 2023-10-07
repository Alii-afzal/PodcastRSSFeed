# from rest_framework_simplejwt.authentication import RefreshTokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import get_authorization_header
from accounts.models import User
from .utils import create_jti, create_access_token, create_refresh_token, cache_key_setter, cache_value_setter
from accounts.serializers import UserRegisterSerializer, UserLoginSerializer
# from accounts.authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from rest_framework import permissions
from django.contrib.auth import authenticate
# from django.core.cache import caches
from rest_framework.exceptions import AuthenticationFailed, APIException
import jwt
import datetime
# from django.conf import settings
from config import settings
    
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(request, email=email, password=password)
        print(user)
        print(request.data)
        # print(serializer.errors)
        if user is None:
            return Response(data={'message': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        jti = create_jti()
        access_token = create_access_token(user.id, jti)
        refresh_token = create_refresh_token(user.id, jti)
        
        key = cache_key_setter(user_id, jti)
        value = cache_value_setter(request)
        refresh_expired_time = settings.REFRESH_EXPIRED_TIME
        # caches.set(key=key, value=value, timeout=refresh_expired_time)
        
        data = {
            "access": access_token,
            "refresh": refresh_token 
        }
        
        return Response(data=data, status=status.HTTP_201_CREATED)


# class RefreshAPIView(APIView):
#     authentication_classes = [RefreshTokenAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request):
#         user = request.issu
#         payload = request.auth
        
#         jti = payload["jti"]
#         chaches['auth'].delete(f"user_{user.id} || {jti}")
        
#         jti = jti_maker()
#         access_token = create_access_token(user_id, jti)
#         refresh_token =create_refresh_token(user_id, jti)
        
#         key = cache_key_setter(user_id, jti)
#         value = cache_value_setter(request)
#         caches["auth"].set(key, value)
        
#         data = {
#             "access": access_token,
#             "refresh": refresh_token
#         }
        
#         return Response(data, status=status.HTTP_201_CREATED)

# class LogoutAPIView(APIView):
#     authentication_classes = [RefreshTokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             payload = request.auth
#             user = request.user
#             jti = payload["jti"]
#             caches['auth'].delete(f"user_{user.id} || {jti}")
            
#             return Response(data={"message":True}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(data={"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
