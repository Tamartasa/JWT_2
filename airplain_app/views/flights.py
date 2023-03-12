
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from airplain_app.models import Flight
from airplain_app.serializers import RegisterSerializer, UserSerializer, FlightSerializer


# Create your views here.
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




# def get_all_flights(request):
#     flights_qs = Flight.objects.all()
#
#     if 'flight_num' in request.query_params:
#         flights_qs = flights_qs.filter(flight_num__exact=request.query_params['flight_num'])
#     if 'origin_city' in request.query_params:
#         flights_qs = flights_qs.filter(origin_city__iexact=request.query_params['origin_city'])
#     if 'destination_city' in request.query_params:
#         flights_qs = flights_qs.filter(destination_city__iexact=request.query_params['destination_city'])
#     if 'date_time_destination' in request.query_params:
#         flights_qs = flights_qs.filter(date_time_destination__lte=request.query_params['date_time_destination'])
#     if 'date_time_origin' in request.query_params:
#         flights_qs = flights_qs.filter(date_time_origin__gte=request.query_params['date_time_origin'])
#     if 'price' in request.query_params:
#         flights_qs = flights_qs.filter(price__lte=request.query_params['price'])
#     if 'is_cancelled' in request.query_params:
#         flights_qs = flights_qs.filter(is_cancelld__exact=request.query_params['is_cancelled'])
#
#     serializer = FlightSerializer(flights_qs, many=True)
#     if not serializer.data:
#         return Response(data=[], status=status.HTTP_204_NO_CONTENT)
#
#     return Response(serializer.data)
#
# # only for logged-in staff!!!
# def add_flight(request):
#     serializer = FlightSerializer(data=request.data, many=False)
#     if serializer.is_valid(raise_exception=True):
#         new_flight = serializer.create(serializer.validated_data)
#         return Response(data=FlightSerializer(new_flight, many=False).data)
#
# @api_view(['GET', 'POST'])
# def flights(request):
#     if request.method == 'GET':
#        return get_all_flights(request)
#     elif request.method == 'POST':
#        return add_flight(request)
#
#
# @api_view(['GET'])
# def get_flight(request, flight_id: int):
#     flight = get_object_or_404(Flight, id=flight_id)
#
#     serializer = FlightSerializer(flight, many=False)
#     return Response(serializer.data)
#
#
