
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from airplain_app.models import Flight
from airplain_app.serializers import RegisterSerializer, UserSerializer, FlightSerializer


# add new flight, update flight - available only for logged-in staff users:
class FlightPermissions(BaseException):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH']:
            return request.user.is_staff and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'PUT', 'DELETE']:
            return request.user.is_authenticated and request.user.is_staff
        return True

class FlightsViewSet(ModelViewSet):
    queryset = Flight.objects.all()

    permission_classes = [FlightPermissions]

    serializer_class = FlightSerializer

# Get all flights or search flight by field
    def get_queryset(self):
        qs = Flight.objects.all()
        if self.action == 'list':
            flight_num = self.request.query_params.get('flight_num')
            if flight_num:
                qs = qs.filter(flight_num__iexact=flight_num)

            origin_city = self.request.query_params.get('origin_city')
            if origin_city:
                qs = qs.filter(origin_city__iexact=origin_city)

            destination_city = self.request.query_params.get('destination_city')
            if destination_city:
                qs = qs.filter(destination_city__iexact=destination_city)

            date_time_destination = self.request.query_params.get('date_time_destination')
            if date_time_destination:
                qs = qs.filter(date_time_destination__gt=date_time_destination)

            date_time_origin = self.request.query_params.get('date_time_origin')
            if date_time_origin:
                qs = qs.filter(date_time_origin__date=date_time_origin)

            price_max = self.request.query_params.get('price_max')
            if price_max:
                qs = qs.filter(price__lte=price_max)

            is_cancelled = self.request.query_params.get('is_cancelled')
            if is_cancelled:
                qs = qs.filter(is_cancelled=is_cancelled)

        return qs

#
