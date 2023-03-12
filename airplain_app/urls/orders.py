from django.urls import path
from rest_framework.routers import DefaultRouter

from airplain_app.views.orders import OrdersViewSet

# automatically defining urls for MoviesViewSet
router = DefaultRouter()
router.register('', OrdersViewSet)


urlpatterns = []

# adding movies urls to urlpatterns
urlpatterns.extend(router.urls)