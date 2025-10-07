from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('movies/', views.MovieListView.as_view(), name='movie-list'),
    path('movies/<int:movie_id>/shows/', views.ShowListView.as_view(), name='show-list'),
    path('shows/<int:show_id>/book/', views.BookShowView.as_view(), name='book-show'),
    path('bookings/<int:booking_id>/cancel/', views.CancelBookingView.as_view(), name='cancel-booking'),
    path('my-bookings/', views.MyBookingsView.as_view(), name='my-bookings'),
]