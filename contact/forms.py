from django import forms
from .models import Contact
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class ContactForm(forms.ModelForm):
    """Форма подписки по email"""
    captcha = ReCaptchaField()

    # TODO http://i.imgur.com/CJgmjnh.png - рассылка по емейл происходит(наша админка видит смс), но нужно настроить почту
    #  через  celery.... Настройка и отправка почты в django - https://youtu.be/9RTZP16rvkQ?t=691

    class Meta:
        model = Contact
        fields = ('email', )
        widgets = {
            "email": forms.TextInput(attrs={"class": "editContent", "placeholder": "Your Email ..."})
        }  # виджет подставляется вместо поля input в template http://i.imgur.com/I6xCg6q.png и для корретно
        # прогрузки формы в html нужно указать его класс что есть в темплейте в поле input
        labels = {
            'email': ''
        }  # http://i.imgur.com/TCtGidw.png


    


