from rest_framework import serializers
from .models import Like, Subscribe, Comment

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'episode', 'user')