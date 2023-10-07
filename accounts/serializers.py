from rest_framework import serializers
from .models import User

# def clean_email(value):
#     if 'admin' in value:
#         raise serializers.ValidationError('admin can`t be in email')

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone_number", "email", "password"]
        extra_kwargs = {
            'password': {'write_only': True},
            # 'email' : {'valiators': (clean_email, )}
        }
    
    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError('username cant be `admin`')
        return value
        
class UserLoginSerializer(serializers.Serializer):
    class Meta:
        model:User
        fields = ["id", "email", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    
    
    

