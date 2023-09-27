from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", 'phone_number', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None) # extracting password form the inputs
        instance = self.Meta.model(**validated_data) # creating the user
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

# class UserRegisterSerializer(serializers.Serializer):
#     phone_number =serializers.CharField(required=True)
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(required=True)