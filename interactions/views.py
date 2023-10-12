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
    authentication_classes = [JWTAuthentication]
    
    def post(self, request):
        episode = Episode.objects.get(id=request.data.get('episode_id'))
        user = request.user
        like, created = Like.objects.get_or_create(user=user, episode=episode)
        if created:
            serializer = self.serializer_class(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            msg = {'status':'This episode is already liked!'}
            return Response(msg, status=status.HTTP_200_OK)
    
    def delete(self, request):
        episode = Episode.objects.get(id=request.data.get('episode_id'))
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
    
    def post(self, request):
        episode = Episode.objects.get(id=request.data.get('episode_id'))
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, episode=episode)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # def post(self, request):
    #     episode = Episode.objects.get(id=request.data.get('episode_id'))
        
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
        
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubscribeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = SubscribeSerializer
    
    x = []
    print(x)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() and serializer.validated_data.get('user') not in self.x:
            
            self.x.append(serializer.validated_data.get('user'))
            
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookMarkAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = BookMarkSerializer
    
    def post(self, request):
        episode = Episode.objects.get(id=request.data.get('episode_id'))
        bookmark_episode, created = BookMark.objects.get_or_create(user=request.user, episode=episode)
        
        if created:
            serialzer = self.serializer_class(bookmark_episode)
            msg= {'status':'Episode Bookmarked.'}
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            msg = {'status':'This episode is already bookmarked'}
            return Response(msg, status=status.HTTP_200_OK)
        
    def delete(self, request):
        episode = Episode.objects.get(id=request.data.get('episode_id'))
        try:
            bookmarked_episode = BookMark.objects.get(user=request.user, episode=episode)
            bookmarked_episode.delete()

            msg = {'status':'No longer bookmarked'}
            return Response(msg, status=status.HTTP_204_NO_CONTENT)
        except BookMark.DoesNotExist:
            msg = {'status':'This episode was not bookmarked'}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)