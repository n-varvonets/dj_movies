from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget  # эта библетеака может загружать также картинкит, а стандартная - только редактировать текстареа

"""для работоспособности редактора ckeditor нужно добавить виджет нашей формы, которая отображается в административной панели"""
# ищем в документации(https://github.com/django-ckeditor/django-ckeditor) раздел Widget и добавляем
class MovieAdminForm(forms.ModelForm):

    description = forms.CharField(widget=CKEditorUploadingWidget())  # важно указать поле, в которые хотим запилить над редактор

    class Meta:
        """данный редактор мы встроем в нашу модель"""
        model = Movie
        fields = '__all__'

    # затем данную форму нам нужно подлкючить к нашему классу


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')  #  позволяет конфигурировать список наших записей(что отображать в админке)... до(http://i.imgur.com/epAlKDe.png) и после(http://i.imgur.com/H5v3LOi.png)
    list_display_links = ('name',)  # нажимая на имя категории мы переходим на нашу запись


# class ReviewInLine(admin.StackedInline): # StackedInline - выводит форму InLine(M2M, FK) вертикально(http://i.imgur.com/xxkuNPj.png)
class ReviewInLine(admin.TabularInline):  # а вот TabularInline - горизонтально(http://i.imgur.com/Yq9PRog.png)
    model = Reviews
    extra = 1  # т.к. по дефолту выводятся 3 доп. поля, а я сейчас всего указываю 1
    readonly_fields = ('name', 'email',)


class MoviesShotsInline(admin.TabularInline):
    """добавим возможность отображатьв нашей модели movie наши кадры (M2M / FK) -  поэтому создаем TabularInline"""
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(
            f'<img src={obj.image.url} width="150" height="auto"')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id',  'category', 'url', 'draft',)
    """можно в админке добавить по чем фильтровать наши записи"""
    list_filter = ('category', 'year')  # http://i.imgur.com/ACSyO0M.png
    """можно в админке добавить поиск наших записей"""
    search_fields = ('title', 'category__name', 'year')  # т.к. категория это обьект(ForeignKey), то нужно указать по какому полю обьекта проводить поиск (http://i.imgur.com/MCqQ49r.png)
    """что бы при отктие нашего фильма мы видели все отзывы прикрепленные к нему(т.к. отзывы это М2М/FK).
    Для этого создадим ниже класс ReviewInLine"""
    inlines = [MoviesShotsInline, ReviewInLine]  # + добавим наш кадры к фильму
    """можно перенсти меню сохранение вверх"""
    save_on_top = True
    """можно настроить сохрнаить обьект как новый обьект, а старый останеться без изенений"""
    save_as = True
    """можно настроить реактирование параметра прямо из спика, для примера возьмум boolean value of draft"""
    list_editable = ('draft',) # до(http://i.imgur.com/iJMv07s.png) и после(http://i.imgur.com/5ZnkNE1.png)
    """можно поля M2M/FK  сделать в одну строку. проблема(http://i.imgur.com/oeYfrJR.png) + можно каким угодно способом гурпировать наши поля + давать именна.. т.е. вместо None  указать имя(http://i.imgur.com/lfKNvsZ.png)"""
    readonly_fields = ('get_image', )

    form = MovieAdminForm  # в нашем классе подключаем выше созданную форму для использования редактора ckeditor... Мол вместо стандартной формы, у нас будет еще с подлюченным редактором ckeditor

    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            # "fields": ("description", "poster")  - это рабочий вариант, но т.к. мы хотим добавить не строку, а картинку, то вызываем наш метод
            "fields": ("description", ("poster",'get_image',))  # ("poster",'get_image',) - поместил в кортеж для того что бы в дашборде можно было добавитть постер и оно отображалось в одну строку
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

    def get_image(self, obj):
        """сделаем так что бы  постеры отображалось"""
        return mark_safe(
            f'<img src={obj.poster.url} width="50" height="auto"')  # и передаем урл нашего постера... для этого изменяем image на poster

    # для того что бы изменить название колонки(http://i.imgur.com/jcu3cH9.png) нужен след метод
    get_image.short_description = 'Poster'


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
    list_display = ("name", "age", 'get_image')  # 4) и затем добавляем имя нашего метода
    readonly_fields = ('get_image', )

    """можно вывести картинку не как строку(http://i.imgur.com/SVxAqbi.png) а как изображение(http://i.imgur.com/X5eykUn.png) - 1) для этого пропишем def get_image(..)"""
    def get_image(self, obj):  # obj - это обьект модели актеров
        return mark_safe(f'<img src={obj.image.url} width="50" height="auto"')  # 2)mark_safe выведит html  не как строку, а как тэг

    get_image.short_description = 'Изображение'  # 3)short_description добавляем описание - так будет называться наш столбец


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", 'get_image' )
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(
            f'<img src={obj.image.url} width="50" height="auto"')

    get_image.short_description = 'Изображение'


# можно изменить вывод титулки в дашборде http://i.imgur.com/MinGgPT.png
admin.site.site_title = "Nick's movies"
admin.site.site_header = "Nick's movies"

# admin.site.register(Category, CategoryAdmin)  # для того что бы класс в админке работал его нужно зарегистровать.... но так же можно регистировать с помощью декоратора
# admin.site.register(Genre)
# admin.site.register(Movie)
# admin.site.register(MovieShots)
# admin.site.register(ActorOrDirector)
# admin.site.register(Rating)
admin.site.register(RatingStar)
# admin.site.register(Reviews)
