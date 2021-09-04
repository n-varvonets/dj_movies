from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Reviews, RatingStar, Rating


class ReviewsForm(forms.ModelForm):
    """Формы отзывов"""

    captcha = ReCaptchaField()  # подключаем поле рекаптчи в форму отправки отзовов

    class Meta:
        """указываем от какое моедли нам строить форму"""
        model = Reviews
        """указываем какие поля будут в нашей форме"""
        fields = ("name", 'email', 'text')  # добавляем в форму отправки отзово наше новое поле

        # форма которую мы использовали для отзовов была просто html(которая рендирилась автоматически) и из-за
        # того что нам нужно добавить рекаптчу, то нам нужно данную форму рендерить и что бы у нас сохранились стили,
        # то мы добавим виджеты к наим полям
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),  # in models.py name = models.CharField("Name", max_length=100)
            "email": forms.EmailInput(attrs={"class": "form-control border"}), # in models.py     name = models.CharField("Name", max_length=100)
            "text": forms.Textarea(attrs={"class": "form-control border"}), # in models    .py  text = models.TextField("Text", max_length=5000)
        }  # attrs то как в  html  django  по умолчяанию его рендерить стиль




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

    """итого у нас получалась форма для заполнения(выбор ModelChoiceField из всех звезд которые мы взяли с с модели RatingStar)"""

