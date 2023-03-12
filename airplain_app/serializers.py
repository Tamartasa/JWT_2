import datetime

from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from airplain_app.models import User, Flight, Order


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'is_staff')


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        # validators=[UniqueValidator(queryset=User.objects.all())]
    )
    # password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'is_staff', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_is_staff(self, value):
        if value and not self.context['request'].user.is_staff:
            raise serializers.ValidationError("You do not have permission to set is_staff to True.")
        return value


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if 'is_staff' in attrs and attrs['is_staff'] and not self.context['request'].user.is_staff:
            raise serializers.ValidationError("You do not have permission to create staff users.")

        return attrs

    def create(self, validated_data):
        is_staff = validated_data.pop('is_staff', False)
        if is_staff and not self.context['request'].user.is_staff:
            raise serializers.ValidationError("You do not have permission to create staff users.")
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=is_staff
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        # Get the flight object from the validated data
        flight = validated_data.get('flight')

        # Calculate the total price based on the number of seats and the seat price of the flight
        number_of_seats = validated_data.get('number_of_seats')

        if number_of_seats > flight.seats_left:
            raise serializers.ValidationError("Not enough seats available for this flight.")
        else:
            seat_price = flight.price
            total_price = number_of_seats * seat_price

            # Set the order_date and total_price fields automatically
            validated_data["order_date"] = datetime.datetime.now()
            validated_data["total_price"] = total_price

            # Create and return the new Order object
            new_order = Order.objects.create(**validated_data)
            return new_order

    def update(self, instance, validated_data):
        if 'number_of_seats' in validated_data or 'flight' in validated_data:
            # Get the new number of seats and the new flight ID
            new_number_of_seats = validated_data.get('number_of_seats', instance.number_of_seats)
            new_flight_id = validated_data.get('flight', instance.flight_id).id

            # Get the new flight object for the new flight ID
            new_flight = Flight.objects.get(id=new_flight_id)

            # Calculate the new total price
            new_total_price = new_number_of_seats * new_flight.price
            instance.total_price = new_total_price
            instance.save()

        return instance
