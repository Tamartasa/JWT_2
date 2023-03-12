from django.urls import path
from rest_framework.routers import DefaultRouter

from airplain_app.views.flights import *

# automatically defining urls for MoviesViewSet
router = DefaultRouter()
router.register('', FlightsViewSet)


urlpatterns = [
    # path('', flights),
    # path('<int:flight_id>', get_flight)
]

# adding movies urls to urlpatterns
urlpatterns.extend(router.urls)
