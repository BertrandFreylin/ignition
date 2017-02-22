from __future__ import unicode_literals

from django.db import models

class Movies(models.Model):
    id = models.IntegerField(primary_key=True, db_column='MovieId')
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)

class Links(models.Model):
    movie = models.ForeignKey(Movies, db_column='MovieId')
    imdb = models.CharField(max_length=20, db_column='imdbId')
    tmdb = models.CharField(max_length=20, db_column='tmdbId')

class Ratings(models.Model):
    user = models.IntegerField(name='userId')
    movie = models.ForeignKey(Movies, db_column='MovieId')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    date = models.IntegerField()

class GenomeTags(models.Model):
    id = models.IntegerField(primary_key=True)
    tag = models.CharField(max_length=255)

class GenomeScores(models.Model):
    movie = models.ForeignKey(Movies, db_column='MovieId')
    tag = models.ForeignKey(GenomeTags)
    relevance = models.CharField(max_length=255)