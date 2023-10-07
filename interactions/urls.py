from django.urls import path
# from .views import like_episode
from .views import LikeAPIView

urlpatterns = [
    path('like/', LikeAPIView.as_view())
    # path('like/<int:episode_id>/', like_episode, name='like_episode'),
    # path('', SubscribeApiView.as_view()),
    # path('', CommentApiView.as_view()),
]
