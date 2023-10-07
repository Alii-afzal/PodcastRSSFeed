import datetime
import jwt
import uuid
from django.conf import settings
from django.core.mail import EmailMessage


def create_access_token(user_id, jti):
    access_token_payload = {
        'token_type':'access',
        'user_id':user_id,
        'exp':datetime.utcnow() + timedelta(seconds=30),
        'iat': datetime.utcnow(), #creation time
        'jti':jti,
    }
    access_token = encode_jwt(access_token_payload)
    return access_token
    
    
       
def create_refresh_token(user_id, jti):
    refresh_token_payload = {
        'token_type':'refresh',
        'user_id':user_id,
        'exp':datetime.utcnow() + timedelta(seconds=30),
        'iat': datetime.utcnow(), #creation time
        'jti':jti,
    }
    refresh_token = encode_jwt(refresh_token_payload)
    return refresh_token

def create_jti():
    return uuid.uuid4().hex

def decode_jwt(token):
    payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
    return payload
    
def encode_jwt(payload):
    token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm=["HS256"])
    return payload
    
def cache_key_setter(user_id, jti):
    return f"user_{user_id} || {jti}"

def cache_value_setter(request):
    return request.META.get('HTTP_USER_AGENT', 'UNKNOWN')

def cache_key_parser(arg):
    return arg.split(" || ")

