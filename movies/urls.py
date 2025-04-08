from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('movies/', views.movie_list, name='movie_list'),
    path('movie/<int:id>/', views.movie_detail, name='movie_detail'),  # Movie detail page

    path('tvshows/', views.tv_show_list, name='tv_show_list'),
]
