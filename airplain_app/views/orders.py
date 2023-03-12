import datetime
from datetime import timezone

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from airplain_app.models import Order, Flight
from airplain_app.serializers import OrderSerializer

# Create your views here.

class OrderPermissions(BaseException):
    def has_permission(self, request, view):
        if request.method in ['POST', 'GET']:
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'PUT', 'GET']:
            return request.user.is_authenticated and request.user.is_staff or\
                request.user.is_authenticated and request.user.id == obj.user_id
        return True

class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()

    permission_classes = [OrderPermissions]

    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action == 'list':
            if 'flight' in self.request.query_params:
                qs = qs.filter(flight=self.request.query_params['flight'])
            if 'user' in self.request.query_params:
                qs = qs.filter(user=self.request.query_params['user'])
            if 'order_date' in self.request.query_params:
                qs = qs.filter(order_date__date=self.request.query_params['order_date'])
            if 'total_price' in self.request.query_params:
                qs = qs.filter(total_price__gt=self.request.query_params['total_price'])
        return qs


