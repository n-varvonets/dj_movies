from django import forms
from .models import Reviews, RatingStar, Rating


class ReviewsForm(forms.ModelForm):
    """Формы отзывов"""
    class Meta:
        """указываем от какое моедли нам строить форму"""
        model = Reviews
        """указываем какие поля будут в нашей форме"""
        fields = ("name", 'email', 'text')


class RatingForm(forms.ModelForm):
    """что бы выводить список добавленных нами звезд мы должны переопределить поле star из model.py"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )  # c помощью ModelChoiceField указываем аттрибуты...
    # 1)queryset - берем все созданные звезды  нашу переменную
    # 2)widget - то как будет представлдена форма html(меняя виджеты - мы можем менять вид внешних форм(выпадающий список или чекбокс или радиобокс))

    class Meta:
        model = Rating
        fields = ("star",)

    """  итого у нас получалась форма для заполнения(выбор ModelChoiceField из всех звезд которые мы взяли с с модели RatingStar)"""

