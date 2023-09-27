from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token

from rest_framework.exceptions import AuthenticationFailed, APIException
import jwt
import datetime
    
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise APIException('User Not Found Error!')
        if not user.check_password(password):
            raise APIException('Incorrect Password Error!')
        
        # serializer = UserSerializer(user)
        # return Response(serializer.data)
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        
        response = Response()
        
        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'token': access_token
        }
        
        return response
    
        

class UserAPIView(APIView):
    def get(self, request):
        auth = get_authorization_header(request).split()
        
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            user = User.objects.filter(pk=id).first()
            return Response(UserSerializer(user).data)
        raise AuthenticationFailed('unauthenticated')  
        
class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshtoken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response(
            {
                'token' : access_token
            }
        )
        
class LogoutAPIView(APIView):
    def post(self, _):
        response = Response()
        response.delete_cookie(key="refreshtoken")
        response.data={
            'message':'success'
        }
        return response