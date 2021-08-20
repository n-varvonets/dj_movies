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

