from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(default='', max_length=150)


class Movie(models.Model):
    title = models.CharField(default='', max_length=150)
    audience = models.IntegerField(default=0)
    poster_url = models.CharField(default='', max_length=300)
    description = models.TextField(default='')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')
    # genre = models.ManyToManyField(Genre, related_name='movies')


class Score(models.Model):
    comment = models.TextField(default='')
    score = models.IntegerField(default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='scores')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scores')