import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_booking.settings')
django.setup()

from booking.models import Movie, Show

def create_sample_data():
    # Create movies
    movies = [
        Movie(title="Avengers: Endgame", duration_minutes=181),
        Movie(title="The Dark Knight", duration_minutes=152),
        Movie(title="Inception", duration_minutes=148),
        Movie(title="Interstellar", duration_minutes=169),
    ]
    
    for movie in movies:
        movie.save()
    
    # Create shows
    shows = []
    for i, movie in enumerate(movies):
        shows.extend([
            Show(
                movie=movie,
                screen_name=f"Screen {j+1}",
                date_time=datetime.now() + timedelta(days=i, hours=j*3),
                total_seats=100,
                available_seats=100
            ) for j in range(3)
        ])
    
    for show in shows:
        show.save()
    
    print("Sample data created successfully!")

if __name__ == "__main__":
    create_sample_data()