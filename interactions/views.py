from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.authentication import JWTAuthentication
from core.models import Channel, Episode
from accounts.models import User
from .models import Like
from .serializers import LikeSerializer, CommentSerializer
# Create your views here.
class LikeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        episode = serializer.validated_data.get('episode')
        # user = User.objects.filter(id=user_id)
        # episode = Episode.objects.filter(id=episode_id)
        like = Like.objects.get_or_create(user=user, episode=episode)

class CommentAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        user = serializer.get
        episode = serializer.get_fields
        
    
    