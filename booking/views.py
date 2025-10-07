from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import User, Movie, Show, Booking
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, 
    MovieSerializer, ShowSerializer, BookingSerializer, BookingCreateSerializer
)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "success", "message": "API is working!"})

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ShowListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShowSerializer
    
    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Show.objects.filter(movie_id=movie_id)

class BookShowView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingCreateSerializer
    
    def post(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        
        serializer = self.get_serializer(data=request.data, context={'show': show})
        serializer.is_valid(raise_exception=True)
        
        seat_number = serializer.validated_data['seat_number']
        
        # Check if seat is already booked
        if Booking.objects.filter(show=show, seat_number=seat_number, status='booked').exists():
            return Response(
                {'error': f'Seat {seat_number} is already booked'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if show has available seats
        if show.available_seats <= 0:
            return Response(
                {'error': 'No available seats for this show'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create booking with transaction for safety
        try:
            with transaction.atomic():
                booking = Booking.objects.create(
                    user=request.user,
                    show=show,
                    seat_number=seat_number,
                    status='booked'
                )
                show.available_seats -= 1
                show.save()
                
                booking_serializer = BookingSerializer(booking)
                return Response(booking_serializer.data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response(
                {'error': 'Booking failed. Please try again.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CancelBookingView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Security check: user can only cancel their own bookings
        if booking.user != request.user:
            return Response(
                {'error': 'You can only cancel your own bookings'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status == 'cancelled':
            return Response(
                {'error': 'Booking is already cancelled'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cancel booking with transaction
        try:
            with transaction.atomic():
                booking.status = 'cancelled'
                booking.save()
                
                # Free up the seat
                booking.show.available_seats += 1
                booking.show.save()
                
                return Response(
                    {'message': 'Booking cancelled successfully'}, 
                    status=status.HTTP_200_OK
                )
                
        except Exception as e:
            return Response(
                {'error': 'Cancellation failed. Please try again.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MyBookingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')