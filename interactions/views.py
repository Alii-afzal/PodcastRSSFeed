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