from django.urls import path
from .views import like_episode

urlpatterns = [
    path('like/<int:episode_id>/', like_episode, name='like_episode'),
    # path('', SubscribeApiView.as_view()),
    # path('', CommentApiView.as_view()),
]
