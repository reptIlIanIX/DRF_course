from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserListAPIView, UsersRegistrationView, UserRetrieveAPIView, UserUpdateAPIView, \
    UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListAPIView.as_view(), name='users'),
    path('register/', UsersRegistrationView.as_view(), name='register'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='detail'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='delete'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]