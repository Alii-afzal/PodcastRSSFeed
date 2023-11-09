from .models import User

from django.contrib.auth.backends import ModelBackend

class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, email, password):
        try:
            user = User.objects.filter(email=email).first()
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return  User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None