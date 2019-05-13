from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(default='', max_length=150)


class Movie(models.Model):
    title = models.CharField(default='', max_length=150)
    summary = models.TextField(default='')
    director = models.CharField(default='', max_length=45)
    audience = models.IntegerField(default=0)
    genre = models.ManyToManyField(Genre, related_name='movies')


class Score(models.Model):
    comment = models.TextField(default='')
    score = models.IntegerField(default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='scores')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scores')