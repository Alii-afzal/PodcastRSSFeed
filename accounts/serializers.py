from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", "email", "password", "full_name"]
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError('username cant be `admin`')
        return value
        
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=60)
    password = serializers.CharField(max_length=60)