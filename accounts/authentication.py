import jwt
from datetime import datetime, timedelta
from rest_framework import exceptions

def create_access_token(id):
    return jwt.encode(
        {
            'user_id':id,
            'exp':datetime.utcnow() + timedelta(seconds=30),
            'iat': datetime.utcnow() #creation time
           
        }, 'access_secret', algorithm='HS256'
    )
    

def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')
        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')   

    
    
def create_refresh_token(id):
    return jwt.encode(
        {
            'user_id':id,
            'exp':datetime.utcnow() + timedelta(days=7),
            'iat': datetime.utcnow() #creation time
           
        }, 'refresh_secret', algorithm='HS256'
    )


def decode_refresh_token(id):
    try:
        payload = jwt.decode(token, 'refresh_secret', algorithms='HS256')
        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')   
