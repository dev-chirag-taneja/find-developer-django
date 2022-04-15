from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import *

urlpatterns = [
    # Authentication
    path('register/', register),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Profile
    path('profiles/', profiles),
    path('profiles/<str:pk>/', profile),
]
