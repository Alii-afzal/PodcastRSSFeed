from django.urls import path
from accounts.views import RegisterAPIView, LoginAPIView, UserAPIView, RefreshAPIView, LogoutAPIView



urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user/', UserAPIView.as_view(), name='user'),
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
]






    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('user/', views.UserView.as_view(), name='user'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),