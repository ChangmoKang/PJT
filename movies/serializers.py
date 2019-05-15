from rest_framework import serializers
from .models import Movie, Score

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['comment', 'score', 'movie', 'user']