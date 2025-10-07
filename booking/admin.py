from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Movie, Show, Booking

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration_minutes', 'created_at']
    search_fields = ['title']

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['movie', 'screen_name', 'date_time', 'total_seats', 'available_seats']
    list_filter = ['screen_name', 'date_time']
    search_fields = ['movie__title']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'show', 'seat_number', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'show__movie__title']