from django.urls import path
from .views import ExtractXMLChannel, ExtractXMLItems, AddPodcastUrlView, UpdatePodcastTaskAPIView, UpdateEpisodesView, AddPodcastAPIView
 
 
urlpatterns = [
    path('extractchannel/', ExtractXMLChannel.as_view()),
    path('extractepisode/', ExtractXMLItems.as_view()),
]
 