from rest_framework import serializers
from .models import Reservation, Room, Hotel
from django.contrib.auth.models import User


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ["name", "updated"]

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user