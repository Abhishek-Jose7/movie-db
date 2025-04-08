import requests
from django.core.files import File
from tempfile import SpooledTemporaryFile
from movies.models import Movie
from django.conf import settings

OMDB_API_KEY = 'd95ce9d5'  # Replace with your actual OMDb API key

def fetch_and_save_poster(movie):
    """Fetch poster from OMDb API and save to movie instance."""
    url = f"http://www.omdbapi.com/?t={movie.title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        poster_url = data.get("Poster")

        if poster_url and poster_url != "N/A":
            # Download the poster image
            image_response = requests.get(poster_url)
            if image_response.status_code == 200:
                # Create a temporary file to hold the image content
                img_temp = SpooledTemporaryFile(max_size=1024*1024, mode='w+b')
                img_temp.write(image_response.content)
                img_temp.flush()  # Ensure the data is written

                # Move to the beginning of the file before saving
                img_temp.seek(0)

                # Create the file and save it to the movie instance
                movie.poster.save(f"{movie.title}_poster.jpg", File(img_temp), save=True)
                print(f"Poster saved for {movie.title}")
            else:
                print(f"Failed to download poster for {movie.title}")
        else:
            print(f"No poster available for {movie.title}")
    else:
        print(f"Failed to retrieve data for {movie.title}")
