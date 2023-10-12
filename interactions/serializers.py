from rest_framework import serializers
from .models import Like, Subscribe, Comment, BookMark

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'episode', 'user')
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'episode')
        
class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('id', 'user', 'channel')
        
class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        exclude = ("user",)