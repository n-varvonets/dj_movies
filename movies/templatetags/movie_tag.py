from django import template
from movies.models import Category, Movie

"""в джанго сществуют два вида template tags:
 1)simple - через вызов метода в темлейте выводит доп дату.
 2)inclusion - умеет рендерить шаблон"""

register = template.Library()

# создадим функцию, которая будет возращать список наших категорий
@register.simple_tag() #обороачиваем её для регистрации нашей функции как темплейтег
def get_categories():
    """example of simple tag -  для вывода всех категрой"""
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_movies(count=5):  # count - стоит по дфеолту 5, мы его получаем из templates/include/sidebar.html(где и рендиряться наши данные) и если изсеним его значение там, то кол-во выводимых фильмов на сайте - изменить
    movies = Movie.objects.order_by('id')[:count]  # сортируем картинки по айди взяв последние пять
    return {'last_movies': movies}  # при вызове данной функции будет возвращать  посл 5ть фильмов

