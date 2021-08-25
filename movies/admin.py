from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')  #  позволяет конфигурировать список наших записей(что отображать в админке)... до(http://i.imgur.com/epAlKDe.png) и после(http://i.imgur.com/H5v3LOi.png)
    list_display_links = ('name',)  # нажимая на имя категории мы переходим на нашу запись


# class ReviewInLine(admin.StackedInline): # StackedInline - выводит форму InLine(M2M, FK) вертикально(http://i.imgur.com/xxkuNPj.png)
class ReviewInLine(admin.TabularInline):  # а вот TabularInline - горизонтально(http://i.imgur.com/Yq9PRog.png)
    model = Reviews
    extra = 1  # т.к. по дефолту выводятся 3 доп. поля, а я сейчас всего указываю 1
    readonly_fields = ('name', 'email',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id',  'category', 'url', 'draft',)
    """можно в админке добавить по чем фильтровать наши записи"""
    list_filter = ('category', 'year')  # http://i.imgur.com/ACSyO0M.png
    """можно в админке добавить поиск наших записей"""
    search_fields = ('title', 'category__name', 'year')  # т.к. категория это обьект(ForeignKey), то нужно указать по какому полю обьекта проводить поиск (http://i.imgur.com/MCqQ49r.png)
    """что бы при отктие нашего фильма мы видели все отзывы прикрепленные к нему(т.к. отзывы это М2М/FK).
    Для этого создадим ниже класс ReviewInLine"""
    inlines = [ReviewInLine]
    """можно перенсти меню сохранение вверх"""
    save_on_top = True
    """можно настроить сохрнаить обьект как новый обьект, а старый останеться без изенений"""
    save_as = True
    """можно настроить реактирование параметра прямо из спика, для примера возьмум boolean value of draft"""
    list_editable = ('draft',) # до(http://i.imgur.com/iJMv07s.png) и после(http://i.imgur.com/5ZnkNE1.png)
    """можно поля M2M/FK  сделать в одну строку. проблема(http://i.imgur.com/oeYfrJR.png) + можно каким угодно способом гурпировать наши поля + давать именна.. т.е. вместо None  указать имя(http://i.imgur.com/lfKNvsZ.png)"""
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster")
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),  # можно такой строчкой сворачивать группу http://i.imgur.com/4csyQzO.png
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )  # http://i.imgur.com/y7XonNo.png


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'movie', 'parent')  # http://i.imgur.com/5WWPKjZ.png
    """можно скрыть от редактирования поля"""
    readonly_fields = ('name', 'email',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(ActorOrDirector)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie")



# admin.site.register(Category, CategoryAdmin)  # для того что бы класс в админке работал его нужно зарегистровать.... но так же можно регистировать с помощью декоратора
# admin.site.register(Genre)
# admin.site.register(Movie)
# admin.site.register(MovieShots)
# admin.site.register(ActorOrDirector)
# admin.site.register(Rating)
admin.site.register(RatingStar)
# admin.site.register(Reviews)
