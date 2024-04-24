from rest_framework import generics, status
from .models import Hotel, Reservation, Room, check_room_availability
from .serializer import HotelSerializer, ReservationSerializer, RoomSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_datetime
from rest_framework.views import APIView
from rest_framework.response import Response



# Bazowa klasa dla APIView z często używanymi metodami
class BaseView:
    permission_classes = [IsAuthenticated]

    def get_object(self, model, pk):
        try:
            return model.objects.get(pk=pk)
        except model.DoesNotExist:
            return None

# Widoki dla Hotel
class HotelList(generics.ListCreateAPIView, BaseView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelDetail(generics.RetrieveUpdateDestroyAPIView, BaseView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

# Widoki dla Reservation
class ReservationList(generics.ListCreateAPIView, BaseView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ReservationDetail(generics.RetrieveUpdateDestroyAPIView, BaseView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

# Widoki dla Room
class RoomList(generics.ListCreateAPIView, BaseView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDetail(generics.RetrieveUpdateDestroyAPIView, BaseView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
# Widok dla strony na której użytkownik dokonuje rejestracji konta    

class Register(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ReservationPlanningAPIView(APIView):
    def post(self, request, *args, **kwargs):
        start_date = parse_datetime(request.POST.get('start_date'))
        end_date = parse_datetime(request.POST.get('end_date'))
        adults = int(request.POST.get('adults', 0))  
        children = int(request.POST.get('children', 0)) 
        
        if not start_date or not end_date:
            return Response({"error": "Invalid dates provided"}, status=400)
        
        if adults < 0 or children < 0:
            return Response({"error": "Number of adults or children cannot be negative"}, status=400)
        
        if start_date >= end_date:
            return Response({"error": "Start date must be before end date"}, status=400)
        
        
        number_of_guests = adults + children
        available_rooms = check_room_availability(start_date, end_date, number_of_guests)
        
        
        serializer = RoomSerializer(available_rooms, many=True)
        return Response(serializer.data)