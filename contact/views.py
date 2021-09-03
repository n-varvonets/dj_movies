from django.shortcuts import render
from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm


class ContactView(CreateView):
    """создадим класс который позволит сохранять нашу форму для раасыылки, которую отправил клиент"""
    model = Contact
    form_class = ContactForm
    # нам нужно будет перенаправить нашего пользователя после успешной отправки формы
    success_url = "/"

