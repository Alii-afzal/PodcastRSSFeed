from datetime import datetime, timedelta
import jwt
import uuid
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.cache import cache

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
        'exp':datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(), #creation time
        'jti':jti,
    }       
    refresh_token = encode_jwt(refresh_token_payload)
    return refresh_token

def create_jti():
    return uuid.uuid4().hex

def decode_jwt(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return payload
    
def encode_jwt(payload):
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token
    
def cache_key_setter(user_id, jti):
    return f"user_{user_id} || {jti}"

def cache_value_setter(request):
    return request.META.get('HTTP_USER_AGENT', 'UNKNOWN')

def cache_key_parser(arg):
    return arg.split(" || ")


def send_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body = data["email_body"],
        to = [data["to_email"]]
    )
    email.send()
    
def cache_refresh_token(refresh_token):
    user_id = refresh_token.get('user_id')
    jti = refresh_token.get('jti')
    exp_date = refresh_token.get('exp')
    iat = refresh_token.get('iat')
    timeout = exp_date - iat

    cache.set(key=jti, value=user_id, timeout=timeout)
    
def check_cache(jti):
    cache_existence = cache.get(jti)
    if bool(cache_existence):
        return cache_existence
    return None

def delete_cache(key):
    cache.delete(f'{key}')


def validate_cached_token(refresh_token):
    jti = refresh_token.get('jti')
    cached_token = check_cache(jti)
    return cached_token


def check_exp_date(exp_date):
    return datetime.now() < exp_date