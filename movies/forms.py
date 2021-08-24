from django import forms
from .models import Reviews


class ReviewsForm(forms.ModelForm):
    """Формы отзывов"""
    class Meta:
        """указываем от какое моедли нам строить форму"""
        model = Reviews
        """указываем какие поля будут в нашей форме"""
        fields = ("name", 'email', 'text')

