from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Movie


# class MoviesView(View):
#     """List of movies"""
#     def get(self, request):
#         """this func proceed get methods и request - это вся информация
#         присланная от клиента(в данном случае от браузрера)"""
#         movies = Movie.objects.all()
#         return render(request, 'movies/movies.html', {'movie_list': movies})  # 3м параметром передаем...
#         #  контекст(, {'movie_list': movies})) - это словарь в котором есть ключи и его значения для темплейта
#
#
# """11111)работющая модель с айди, но мы шв в нашей модели указали url конкретного выльма через slug..."""
# # class MovieDetailView(View):
# #     """Full description of movie"""
# #     def get(self, request, pk):  # pk - некое число, которое мы перендаем из url
# #         movie = Movie.objects.get(id=pk)  # method get received ONLY one record (by pk)
# #         print(movie.title, pk)
# #         return render(request, 'movies/movie_detail.html', {'movie': movie})  # 3м параметром передаем...
# """т.е. теперь сохраним наш атрибут url модели movie  не через переданный id, а через через slug"""
# class MovieDetailView(View):
#     """Full description of movie"""
#     def get(self, request, slug):  # pk - некое число, которое мы перендаем из url
#         movie = Movie.objects.get(url=slug)  # method get received ONLY one record (by pk)
#         print(movie.url, 'and slug is ... = ', slug)
#         return render(request, 'movies/movie_detail.html', {'movie': movie})  # 3м параметром передаем...


"""2222)rewrite above funcs using ListView и DetailView"""
class MoviesView(ListView):
    """List of movies  - в данном класе нужно указать: модель, набор уже конкретных
    данных с которыми работаем и темлейт в который эти данные вкладываем"""
    model = Movie
    # queryset = Movie.objects.all()  # но у нас не должно ваыводиться поле такое как draft(черновик)... ниже строчкой это правим
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movies.html"


class MovieDetailView(DetailView):
    """Full description of movie"""
    model = Movie
    slug_field = 'url'  # в данном классе мы не указываем наш темлейт, потому что джанго будет автоматически искать
    # шаблон  movie_detail... он строит наш шаблон так <model>_detail -  а выше в MoviesView мы его указали, потому
    #  наше имя шаблона отличается от стандартного постороения <model>_list


