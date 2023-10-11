from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Like, Comment, Subscribe, BookMark

from .serializers import LikeSerializer, CommentSerializer, SubscribeSerializer, BookMarkSerializer
from core.models import Channel, Episode
from accounts.authentication import JWTAuthentication


class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    
    def post(self, request, episode_id):
        episode = Episode.objects.get(id=episode_id)
        user = request.user
        
        like, created = Like.objects.get_or_create(user=user, episode=episode)
        if existing_like:
            serializer = self.serializer_class(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            msg = {'status':'This episode is already liked!'}
            return Response(msg, status=status.HTTP_200_OK)
    
    def delete(self, request, episode_id):
        episode = PodcastEpisodeData.objects.get(id=episode_id)
        try:
            like = Like.objects.get(user=request.user, episode=episode)
            like.delete()
            msg = {'status':'Unliked!'}
            return Response(msg, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            msg = {'status':'This episode is not liked!'}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        
class CommentAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = CommentSerializer
    def post(self, request, episoe_id):
        episode = Episode.objects.get(id=episoe_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubscribeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = SubscribeSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)