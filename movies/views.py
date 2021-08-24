from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Movie
from .forms import *


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

"""раб. способ отправки формы отзыва через обычный View"""
# class AddReview(View):
#     """Отзывы. Т.к. в UI темлейта используем метод пост для заполнения формы, то нужно его обработать"""
#     def post(self, request, pk):
#         # print(request.POST)  # <QueryDict: {'csrfmiddlewaretoken': ['AYUeKVEVCOLKBhpsp8ctwXfbZLfZaXnTvhjhSYt0OJrlyvM1fj1Qg7WOTnYSimWa'], 'text': ['qweqw'], 'name': ['new'], 'email': ['agent@agent.com']}>
#         return redirect('/')
"""но можно  и через импорт формы с forms.py c уже указанной моделью и её полями"""
class AddReview(View):
    def post(self, request, pk):
        form = ReviewsForm(request.POST)  # таким способом джанго запонит наши данные, которые пришли с формы
        """1) крутой способ назанчения полю movie наш обьект фильма с помощью числа(id)"""
        # if form.is_valid():  # дальше мы можем проверить её на валидность и если все ок, то сохраняем её
        #     """но т.к. у нас отзыв првязывается на определенный фильм, то нам нужно так же указать к какмоу фильму привязывать наш отзыв"""
        #     form = form.save(commit=False)  # этой строкой мы говорим что хотим приоставновить сохранение нашкей формы, что внести некие измения в нее перед занисением в бд
        #     """в поле  movie мы можем должны фильм, к которому нужно привязаться, но т.к. у нас есть только pk нашего
        #      фильма, то напрямую в это поле мы не можем передать данное число - мы должны передавать обьект фильма...
        #      это можно сделать через нижнее подчеркивание, потому что есть ForeignKey http://i.imgur.com/3QTCSsU.png"""
        #     form.movie_id = pk
        #     form.save()
        # return redirect('/')
        """2) второй крутой способ назанчения полю movie наш обьект фильма не с помощью числа(id), а с помощью обьекта"""
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())  # get_absolute_url - для реидректа на ту же самую страницу после остановления комента(поста формы)

