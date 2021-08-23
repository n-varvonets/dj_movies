from django.shortcuts import render
from django.views.generic.base import View
from .models import Movie


class MoviesView(View):
    """List of movies"""
    def get(self, request):
        """this func proceed get methods и request - это вся информация
        присланная от клиента(в данном случае от браузрера)"""
        movies = Movie.objects.all()
        return render(request, 'movies/movies.html', {'movie_list': movies})  # 3м параметром передаем...
        #  контекст(, {'movie_list': movies})) - это словарь в котором есть ключи и его значения для темплейта


class MovieDetailView(View):
    """Full description of movie"""
    def get(self, request, pk):  # pk - некое число, которое мы перендаем из url
        movie = Movie.objects.get(id=pk)  # method get received ONLY one record (by pk)
        print(movie.title, pk)
        return render(request, 'movies/movie_detail.html', {'movie': movie})  # 3м параметром передаем...
        #  контекст(, {'movie_list': movies})) - это словарь в котором есть ключи и его значения для темплейта

