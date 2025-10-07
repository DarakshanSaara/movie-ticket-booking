from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Movie, Show, Booking

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        
        return data

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'duration_minutes', 'created_at']

class ShowSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    booked_seats = serializers.SerializerMethodField()
    
    class Meta:
        model = Show
        fields = ['id', 'movie', 'movie_title', 'screen_name', 'date_time', 'total_seats', 'available_seats', 'booked_seats']
    
    def get_booked_seats(self, obj):
        return list(obj.bookings.filter(status='booked').values_list('seat_number', flat=True))

class BookingSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='show.movie.title', read_only=True)
    screen_name = serializers.CharField(source='show.screen_name', read_only=True)
    show_time = serializers.DateTimeField(source='show.date_time', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'show', 'movie_title', 'screen_name', 'show_time', 'seat_number', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']

class BookingCreateSerializer(serializers.Serializer):
    seat_number = serializers.IntegerField(min_value=1)
    
    def validate_seat_number(self, value):
        show = self.context['show']
        if value > show.total_seats:
            raise serializers.ValidationError(f'Seat number must be between 1 and {show.total_seats}')
        return value