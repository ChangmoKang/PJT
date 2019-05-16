from django.contrib import admin
from .models import Genre, Movie, Score, StillCut

# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Score)
admin.site.register(StillCut)