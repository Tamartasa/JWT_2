from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from airplain_app.views.auth import *

urlpatterns = [
    path('signup/', sign_up),
    path('data/', get_user_data),
    path('users/', get_all_users),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]