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

from django.utils.translation import gettext_lazy as _


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
    
class SubscribeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribeSerializer
    query_set = Subscribe.objects.all()
    
    def post(self, request):
        channel_id = request.data.get('channel')
        user = request.user

        existing_subscription = Subscribe.objects.filter(user=user, channel=channel_id).first()

        if existing_subscription:
            return Response({'message': _("Subscription already exists.")}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


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
        
# class RecommendationView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         user = request.user
#         max_count = Recommendation.objects.filter(user=user).aggregate(max_count=Max("count"))["max_count"]
#         flatlist = set()
        
#         if max_count != 0:
#             recommendation_query = Recommendation.objects.filter(user=user, count=max_count)
#             unique_category_ids = recommendation_query.values_list('category', flat=True).distinct()
#             channels = Channel.objects.filter(xml_link__categories__in=unique_category_ids)
#             flatList.update(channels)

#         ser_data = ChannelSerializer(flatList, many=True, context={"request": request})

#         return Response(ser_data.data, status=status.HTTP_200_OK)