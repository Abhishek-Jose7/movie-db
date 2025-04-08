from django.shortcuts import render, get_object_or_404
from .models import Movie, TVShow

def home(request):
    random_movies = Movie.objects.order_by('?')[:10]  # Fetch 10 random movies
    return render(request, 'movies/home.html', {'random_movies': random_movies})


def movie_list(request):
    # Fetch all movies from the database
    movies = Movie.objects.all()
    # Pass the movies to the template
    return render(request, 'movies/movie_list.html', {'movies': movies})

def tv_show_list(request):
    tv_shows = TVShow.objects.all()
    return render(request, 'movies/tv_show_list.html', {'tv_shows': tv_shows})

def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, 'movies/movie_detail.html', {'movie': movie})