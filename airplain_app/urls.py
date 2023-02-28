from django.urls import path

from airplain_app.views import *

urlpatterns = [
    path('sign_up/', sign_up),
    # path('me/', get_logged_in_user_data),
    # path('version/', get_version),
]