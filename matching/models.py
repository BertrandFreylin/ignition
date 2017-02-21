from __future__ import unicode_literals

from django.db import models

class Movies(models.Model):
    id = models.AutoField(primary_key=True, db_column='MovieId')
    title = models.CharField(max_length=158)
    genres = models.CharField(max_length=77)

class Links(models.Model):
    movie = models.ForeignKey(Movies, db_column='MovieId')
    imdb = models.IntegerField(db_column='imdbId')
    tmdb = models.CharField(max_length=6, db_column='tmdbId')

class Ratings(models.Model):
    user = models.IntegerField(name='userId')
    movie = models.ForeignKey(Movies, db_column='MovieId')
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    date = models.IntegerField()

class Tags(models.Model):
    user = models.IntegerField(name='userId')
    movie = models.ForeignKey(Movies, db_column='MovieId')
    tag = models.CharField(max_length=55)
    date = models.IntegerField()