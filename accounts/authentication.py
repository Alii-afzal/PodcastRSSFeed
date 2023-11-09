import jwt
from rest_framework import exceptions
from rest_framework import authentication
from django.contrib.auth.backends import BaseBackend
from django.conf import settings
# from django.core.cache import caches
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        """
            Extract the JWT from the Authorization header
        """

        authoriztion_header = request.META.get('HTTP_AUTHORIZATION')
        try:
            token = self.get_the_token_from_header(authoriztion_header)
            if not token:
                return None, None
        except:
            return None, None

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise exceptions.AuthenticationFailed('Invalid signature')
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Access token expired')
        except:
            raise exceptions.AuthenticationFailed("Invalid token")
        
        jti = payload.get("jti")
        
        # if not caches.get(jti):
        #     raise exceptions.AuthenticationFailed("Invalid token")
        
        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if user is None:
                raise user.DoesNotExist["User not found"]
            return user, None
        except:
            raise exceptions.AuthenticationFailed("User id not found in JWT")
    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')
        return token

