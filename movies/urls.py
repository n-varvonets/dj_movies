from django.urls import path
from . import views

urlpatterns = [
    path('', views.MoviesView.as_view()),
    # path('<int:pk>/', views.MovieDetailView.as_view()),  модель без url and slug, а только через его id
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),  # данный slug будет ппередан в метод  get into view.py -  а slug -  это уже не int ,а str взятая
]

