import requests
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre
from .fetch_posters import fetch_and_save_poster  # Import fetch_and_save_poster from fetch_posters.py

API_KEY = 'd95ce9d5'  # Replace with your OMDb API key

def get_popular_movies(page=1):
    """Fetch popular movies from OMDb API."""
    url = f"http://www.omdbapi.com/?s=movie&apikey={API_KEY}&page={page}"  # Fetch movies (modify query here if needed)
    response = requests.get(url)
    data = response.json()

    if data.get('Response') == 'True':
        return data.get('Search', [])
    else:
        print(f"Error fetching data: {data.get('Error')}")
        return []

def add_movie_to_db(title):
    """Add a movie to the database, including ratings and other details."""
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get('Response') == 'True':
        # Fetch or create genre
        genre_name = data.get('Genre', '').split(',')[0].strip()
        genre, created = Genre.objects.get_or_create(name=genre_name)

        # Extract rating (you can choose the rating you need, e.g., IMDb rating)
        # Assuming you want the IMDb rating
        
        # Create or update movie
        movie, created = Movie.objects.get_or_create(
            title=data.get('Title'),
            year=data.get('Year'),
            description=data.get('Plot'),
            genre=genre,
            rating=data.get('imdbRating')
        )

        # Fetch and save poster
        fetch_and_save_poster(movie)  # This should be passed the movie object, not the URL

        if created:
            print(f"Added {data.get('Title')} to the database.")
        else:
            print(f"Updated {data.get('Title')} in the database.")
    else:
        print(f"Movie {title} not found.")

class Command(BaseCommand):
    help = 'Imports movies and genres from OMDb API'

    def handle(self, *args, **kwargs):
        page = 1
        total_movies_added = 0

        while True:
            # Fetch movies for the current page
            movies = get_popular_movies(page)
            
            if not movies:
                break  # Stop if no movies are found

            for movie in movies:
                title = movie.get('Title')
                if title:
                    add_movie_to_db(title)
                    total_movies_added += 1
            
            page += 1  # Move to the next page

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {total_movies_added} movies and genres'))
