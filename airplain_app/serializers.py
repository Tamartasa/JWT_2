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
    class Meta:
        model = Order
        fields = "__all__"