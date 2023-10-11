from django.urls import path
# from .views import like_episode
from .views import LikeAPIView

urlpatterns = [
    path('like/', LikeAPIView.as_view())
]