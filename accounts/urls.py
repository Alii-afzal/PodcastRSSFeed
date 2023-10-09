from django.urls import path
from accounts.views import RegisterAPIView, LoginAPIView, AuthenticatedView, RefreshAPIView, LogoutAPIView
# , UserAPIView, RefreshAPIView, LogoutAPIView


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('jwtauthenticate/', AuthenticatedView.as_view()),
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]