from django.urls import path
# from .views import like_episode
from .views import LikeAPIView, CommentAPIView, SubscribeAPIView, BookMarkAPIView

urlpatterns = [
    path('like/', LikeAPIView.as_view()),
    path('comment/', CommentAPIView.as_view()),
    path('subscribe/', SubscribeAPIView.as_view()),
    path('bookmark/', BookMarkAPIView.as_view()),
]