from django.db import models
from datetime import date

from django.urls import reverse


class Category(models.Model):
    """Categories"""
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        """контейнер класса с метаданными прикрипленными к модели. Он определяет такие вещи как:
            - имя связанной таблицы с бд
            - является ли модель абстрактная
            - единственное и множественное число имени"""
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class ActorOrDirector(models.Model):
    """Person as actor or director"""
    name = models.CharField("Name of person", max_length=150)
    age = models.PositiveSmallIntegerField("Age", default=0)
    description = models.TextField("Description")
    image = models.ImageField("Person's image", upload_to="actors_directors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Actor or director"
        verbose_name_plural = "Actors or directors"


class Genre(models.Model):
    """Genre"""
    name = models.CharField("Name of genre", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Movie(models.Model):
    """Movies"""
    title = models.CharField("Title", max_length=100)
    tagline = models.CharField("Tagline", max_length=100, default='')  # по умолчание - пустое
    description = models.TextField("Description")
    poster = models.ImageField("Poster", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Realise date", default=2021)
    country = models.CharField("Country", max_length=30)
    directors = models.ManyToManyField(ActorOrDirector, verbose_name="director", related_name="film_director")
    actors = models.ManyToManyField(ActorOrDirector, verbose_name="actor", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Genre")
    world_premiere = models.DateField("World premiere", default=date.today)
    budget = models.PositiveSmallIntegerField("Budget", default=0, help_text="Indicate the price in USA currency")
    fees_in_usa = models.PositiveSmallIntegerField("Fees in USA", default=0, help_text="USA currency")
    fees_in_world = models.PositiveSmallIntegerField("Fees in world", default=0, help_text="USA currency")
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Draft', default=False)

    def get_absolute_url(self):  # создаем абс урл котнкретного фильма и вызываем его в movies.movie_list  для переходжа из всего всписка на наш кокретный фильм
        return reverse("movie_detail", kwargs={"slug": self.url})  # передаем темлейт, в который запихываем наш url, а слаг - это для urls.py

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"


class MovieShots(models.Model):
    """Movie shots"""
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description")
    image = models.ImageField("Image of movies", upload_to="movies_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Movie shot"
        verbose_name_plural = "Movie shots"


class RatingStar(models.Model):
    """Star of rating"""
    value = models.SmallIntegerField("Value", default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Star of rating"
        verbose_name_plural = "Stars of rating"


class Rating(models.Model):
    """Rating"""
    ip = models.CharField("IP address", max_length=15)
    star = models.ForeignKey(RatingStar, verbose_name="Star", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Reviews(models.Model):
    """Reviews"""
    email = models.EmailField()
    name = models.CharField("Name", max_length=100)
    text = models.TextField("Text", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True
    )  # т.е. запись будет ссылаться на запись в этой же таблице
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"