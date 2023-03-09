# from django.contrib.auth.models import User
# from django.shortcuts import render
# from rest_framework import status
# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.generics import get_object_or_404
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.response import Response
# from rest_framework_simplejwt.authentication import JWTAuthentication
#
# from airplain_app.models import Flight
# from airplain_app.serializers import RegisterSerializer, UserSerializer, FlightSerializer
#
#
# # Create your views here.
#
#
#
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
#         flights_qs = flights_qs.filter(date_time_otigin__gte=request.query_params['date_time_origin'])
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
#
