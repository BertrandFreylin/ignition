from django.conf.urls import url
from matching.utils import get_movies, find_movies
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^get_movies/', get_movies, name='get_movies'),
    url(r'^find_movies/', find_movies, name='find_movies'),
]