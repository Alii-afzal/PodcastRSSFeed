from django.urls import path
from .views import ExtractXMLChannel, ExtractXMLItems, AddPodcastUrlView, UpdatePodcastTaskAPIView, UpdateEpisodesView, AddPodcastAPIView
 
 
urlpatterns = [
    path('extractchannel/', ExtractXMLChannel.as_view()),
    path('extractepisode/', ExtractXMLItems.as_view()),
    path('addpodcastadmin/', AddPodcastUrlView.as_view()),
    path('update_episode/', UpdateEpisodesView.as_view()),
    path('update_task_episode/', UpdatePodcastTaskAPIView.as_view()),
]
 