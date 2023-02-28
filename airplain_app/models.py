from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class Flight(models.Model):

    flight_number = models.CharField(db_column="flight_number", max_length=150, null=False, blank=False)
    origin_country = models.CharField(db_column="origin_country", max_length=256, null=False, blank=False)
    origin_city = models.CharField(db_column="origin_city", max_length=256, null=False, blank=False)
    origin_airport_code = models.CharField(db_column="origin_airport_code", max_length=256, null=True, blank=True)
    destination_country = models.CharField(db_column="destination_country", max_length=256, null=False, blank=False)
    destination_city = models.CharField(db_column="destination_cityy", max_length=256, null=False, blank=False)
    destination_airport_code = models.CharField(db_column="destination_airport_code", max_length=256, null=True, blank=True)
    date_time_origin = models.DateTimeField(db_column="date_time_origin", null=False, blank=False)
    date_time_destination = models.DateTimeField(db_column="date_time_destination", null=False, blank=False)
    total_num_of_seats = models.IntegerField(db_column="total_num_of_seats", null=False, blank=False)
    seats_left = models.IntegerField(db_column="seats_left", null=False, blank=False)
    is_cancelled = models.BooleanField(db_column="is_cancelled", null=True, blank=True, default=False)
    price = models.IntegerField(db_column="price", null=False, blank=False)

    class Meta:
        db_table = 'flights'


class Order(models.Model):

    flight_id = models.ForeignKey(Flight, on_delete=models.RESTRICT)
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    number_of_seats = models.IntegerField(db_column="number_of_seats", null=False, blank=False,
                                          validators=[MinValueValidator(0)])
    order_date = models.DateTimeField(db_column="order_date", null=False, blank=False)
    total_price = models.IntegerField(db_column="total_price", null=False, blank=False)

    class Meta:
        db_table = 'orders'

# class User(models.Model):
#
#     first_name = models.CharField(db_column="first_name", max_length=256, null=False, blank=False)
#     last_name = models.CharField(db_column="last_name", max_length=256, null=False, blank=False)
#     username = models.CharField(db_column="username", max_length=256, null=False, blank=False)
#     is_staff = models.BooleanField(db_column="is_staff", null=False, blank=False)
#
#     class Meta:
#         db_table = 'users'