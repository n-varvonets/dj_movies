from django.urls import path
from . import views

urlpatterns = [
    path('', views.MoviesView.as_view()),
    # path('<int:pk>/', views.MovieDetailView.as_view()),  модель без url and slug, а только через его id
    path('filter/', views.FilterMoviesView.as_view(), name='filter'), #  path('<filter>/' был поставлен выше path('<slug:slug>/', для того что бы поиск по path('<filter>/', не попдал под шаблон поиска по слагу
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),  # данный slug будет ппередан в метод  get into view.py -  а slug -  это уже не int ,а str взятая
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('actor-or-director/<str:slug>/', views.ActorOrDirectorView.as_view(), name='actor_or_director_detail'),
]

