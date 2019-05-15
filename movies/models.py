from django.db import models
from django.conf import settings


class Genre(models.Model):
    genreNm = models.CharField(default='', max_length=150)
    selected = models.BooleanField(default=False)


class Nation(models.Model):
    nationNm = models.CharField(default='', max_length=150)


class Director(models.Model):
    peopleNm = models.CharField(default='', max_length=150)


class Actor(models.Model):
    peopleNm = models.CharField(default='', max_length=150)


class StillCut(models.Model):
    stillCut = models.CharField(default='', max_length=150)


class Movie(models.Model):
    movieCd = models.IntegerField(default=0)
    movieNm = models.CharField(default='', max_length=150)
    openDt = models.CharField(default='', max_length=150)
    audiAcc = models.IntegerField(default=0)
    movieNmEn = models.CharField(default='', max_length=150)
    showTm = models.IntegerField(default=0)
    posterUrl = models.CharField(default='', max_length=200)
    description = models.TextField(default='')
    score = models.FloatField(default=0)
    trailer = models.CharField(default='', max_length=150)
    genre = models.ManyToManyField(Genre, related_name='movies')
    nation = models.ManyToManyField(Nation, related_name='movies')
    director = models.ManyToManyField(Director, related_name='movies')
    actor = models.ManyToManyField(Actor, related_name='movies')
    stillCut = models.ManyToManyField(StillCut, related_name='movies')
    selected = models.BooleanField(default=False)
    
    def __str__(self):
        return self.movieNm
    

class Score(models.Model):
    comment = models.TextField(default='')
    score = models.IntegerField(default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='scores')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scores')