from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Movie, Category, ActorOrDirector, Genre
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

"""можно передавть данные в наши шаблоны не используя темлейт теги, а этом файле view создать класс и 
потом где нужны доп данные, просто наследовть его в этих моделях импользуя созданные методы в классе(def get_context_dat) и юзать их в наших темплейтах"""
class GenreYear():
    # TO DO не пониманию почему мы обращаемся к view в темплейте
    # "view" у нас из context-а. В ContextMixin в методе get_context_data в context добавляют аттрибут "view" для темлейта
    """Жанры и года фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        """получаем все года фильмов(не черновик)и с помощью  values забираем из списка фильмов только поле year"""
        return Movie.objects.filter(draft=False).values('year')
    

"""2222)rewrite above funcs using ListView и DetailView"""
class MoviesView(GenreYear, ListView):
    """List of movies  - в данном класе нужно указать: модель, набор уже конкретных
    данных с которыми работаем и темлейт в который эти данные вкладываем"""
    model = Movie
    # queryset = Movie.objects.all()  # но у нас не должно ваыводиться поле такое как draft(черновик)... ниже строчкой это правим
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movies.html"

    #  гвоорит нам какое кол-во стр
    paginate_by = 3


    def get_context_data(self, *args, **kwargs):
        """для того что бы странице списка фильмов вывести дополнительно категории в нашем классе MoviesView,
        то нам нужно добавить этот метод"""
        context = super().get_context_data(*args, **kwargs) #  вызвав метод super нашего родителя мы получаем словарбь данный и занисим его в переменную  context
        context['categories'] = Category.objects.all()  # в соварь данный заносим новую пару ключ значение с нашими полученными категориями
        return context



class MovieDetailView(GenreYear, DetailView):
    """Full description of movie"""
    model = Movie
    slug_field = 'url'  # в данном классе мы не указываем наш темлейт, потому что джанго будет автоматически искать
    # шаблон  movie_detail... он строит наш шаблон так <model>_detail -  а выше в MoviesView мы его указали, потому
    #  наше имя шаблона отличается от стандартного постороения <model>_list

    def get_context_data(self, **kwargs):
        """передаем созданную форму с нашими зевздами в  шаблон/темплейт по ключу star_form"""
        context = super().get_context_data(**kwargs)  #  в переменную  context заносим работу родительского метода  get_context_data
        context['star_form'] = RatingForm()

        return context

    """рабочий метод для отображения катемгорий на страницу описания фильма, но он нарушвет DRY... для избежание этого:
    1) сделать клас Mixin и занемти внего данный метод  и потом наследовать данн ый класс Mixins.
    2)  создать отдельный темплейт тег(вот это мы и сделаем)"""
    # def get_context_data(self, *args, **kwargs):
    #     """the same method as in MovieDetailView above this"""
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context

"""раб. способ отправки формы отзыва через обычный View"""
# class AddReview(View):
#     """Отзывы. Т.к. в UI темлейта используем метод пост для заполнения формы, то нужно его обработать"""
#     def post(self, request, pk):
#         # print(request.POST)  # <QueryDict: {'csrfmiddlewaretoken': ['AYUeKVEVCOLKBhpsp8ctwXfbZLfZaXnTvhjhSYt0OJrlyvM1fj1Qg7WOTnYSimWa'], 'text': ['qweqw'], 'name': ['new'], 'email': ['agent@agent.com']}>
#         return redirect('/')
"""но можно  и через импорт формы с forms.py c уже указанной моделью и её полями"""


class AddStarRating(View):
    '''Добавленипе рейтинга к фильму'''
    def get_client_ip(self, request):
        """получаем ip нашего клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)

        """когда к нам придет пост запрос, тогда в нашу форму мы пердадим полунные данные с поста"""
        if form.is_valid():
            """т.к. один и тот же клиент не может устноватить разные рейтинги к оденому фильму"""
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),  # в данном методе мы будем получать айли клиента, который отправил нам запрос
                movie_id=int(request.POST.get("movie")),  #  в данное поле мы передаем поле movie  из нашего  post запроса... эти данные на приходят с нашего скрытого поля movie в templates.movie_detail
                defaults={'star_id': int(request.POST.get('star'))}  # (поле /radio  значения самой звезды) в наше поле мы должны
                # перебрать словарь и ключ того значения, которое хотим изменить и значение на которое мы меняешм в том случае если
                # найлем такую запись. Т.е. если такая запись будет найдена, то у нас только поменяется значение звезды, а муви и айпи - остануться
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(staus=400)



class AddReview(View):
    def post(self, request, pk):
        form = ReviewsForm(request.POST)  # таким способом джанго запонит наши данные, которые пришли с формы
        """1) крутой способ назанчения полю movie наш обьект фильма с помощью числа(id)"""
        # if form.is_valid():  # дальше мы можем проверить её на валидность и если все ок, то сохраняем её
        #     """но т.к. у нас отзыв првязывается на определенный фильм, то нам нужно так же указать к какмоу фильму привязывать наш отзыв"""
        #     form = form.save(commit=False)  # этой строкой мы говорим что хотим приоставновить сохранение нашкей формы, что внести некие измения в нее перед занисением в бд
        #     """в поле  movie мы можем должны фильм, к которому нужно привязаться, но т.к. у нас есть только pk нашего
        #      фильма, то напрямую в это поле мы не можем передать данное число - мы должны передавать обьект       фильма...
        #      это можно сделать через нижнее подчеркивание, потому что есть ForeignKey http://i.imgur.com/3QTCSsU.png"""
        #     form.movie_id = pk
        #     form.save()
        # return redirect('/')
        """2) второй крутой способ назанчения полю movie наш обьект фильма не с помощью числа(id), а с помощью обьекта"""
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            """для того случая когда кто-то ответить на отзыв, то нужно призначить нашему отзову конкретного олдителя(ту
             id  записиЮ к кторой обращаться)  в нашем подзапросе мы будем искать ключ parent(имя нашего поля) и если 
             оно будет, то выолненим данный код, он будет отсутвовать, то подставим  None и наш отзыв будет без родителя, т.е. начальный"""
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())  # get_absolute_url - для реидректа на ту же самую страницу после остановления комента(поста формы)


class ActorOrDirectorView(GenreYear, DetailView):
    """Вывод инофрмации об актере"""
    model = ActorOrDirector
    template_name = 'movies/actors_or_directors.html'

    # подбирается слаг нашего конкретного обьекта фильма по его имени, что бы потом можног было подставить его в url вместо id
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):

    # добавим что бы при фильтре жанров фильмов в сайдбаре выводило бы пагинацию
    paginate_by = 1

    template_name = 'movies/movies.html'


    def get_queryset(self):
        """возращаем queryset там где года будут входить в список, который будет возвращаться с фронтенда"""
        # queryset = Movie.objects.filter(
        #     year__in=self.request.GET.getlist("year"),
        #     genres__in=self.request.GET.getlist("genre")
        # ) в данном queryset запятая - это логическое условие, что у нас олжен совпадать и год и жанр одновременно
        """ниже способом делаем уже условие и/или"""
        # queryset = Movie.objects.filter(
        #     Q(year__in=self.request.GET.getlist("year")) |
        #     Q(genres__in=self.request.GET.getlist("genre"))
        # )
        """правильный фильтр...
        фильтровать по одному фильтру, если выбран только один, и фильтровать по двум параметрам, если выбраны два"""
        queryset = Movie.objects.all()
        if "year" in self.request.GET:
            queryset = queryset.filter(year__in=self.request.GET.getlist("year"))
        if "genre" in self.request.GET:
            queryset = queryset.filter(genres__in=self.request.GET.getlist("genre"))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(FilterMoviesView, self).get_context_data(*args, **kwargs)
        #  в данный конекст мы добваим два ключа (года и жанры)
        #  что бы мы могли передавть в шаблон для подставки в урл пагинации выбранный фильтр

        """т.к. нам приходит список выбранных готов или жанров, то из данного риквеста мы можем зараннее сформировать
         завдовомо верную ссылку что бы в темплейте её просто подставитбь в урл пагинации"""
        context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist("year")])  # приходит список выбранных при фильтре в сайдбаре годов от клиента
        context['genre'] = ''.join([f'genre={x}&' for x in self.request.GET.getlist("genre")])
        return context


class Search(GenreYear, ListView):
    """Организуем класс для нашего поиска"""

    template_name = 'movies/movies.html'

    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('search-input-q'))  # 1)фильтруем наши фильмы по полю title , которое доставли из ключа search-input-q
        # 2)применяем доп.параметр __icontains для того что бы у нас не учитывался регистр
        # 3)сравниваем по тем параметрам которые к нам пришли

    def get_context_data(self, *args, **kwargs):
        context = super(Search, self).get_context_data(*args, **kwargs)
        """для работы пагинации лобавляем ключ, который передадим в наш темлейт + не забудь указать новый укл для поиска"""
        # context['key-search-q-for-pagination'] = self.request.GET.get('search-input-q')
        """что бы в темплейте не писать в темлейте правильную ссылку подобным образом  как для строки выше, 
        <a href="?q={{ q }}&{{ genre }}{{ year }}page=1">1</a> , то можно сразу сгенерить ссылку здесь"""
        context['key_search_q_for_pagination'] = f"q={self.request.GET.get('search-input-q')}&"
        return context



