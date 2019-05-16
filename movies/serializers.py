from rest_framework import serializers
from .models import Genre, Nation, Director, Actor, StillCut, Movie, Score
from django.contrib.auth import get_user_model


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class NationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nation
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'
        
        
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'
        
    
class StillCutSerializer(serializers.ModelSerializer):
    class Meta:
        model = StillCut
        fields = '__all__'
        

class MovieSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(many=True)
    nation = serializers.StringRelatedField(many=True)
    director = serializers.StringRelatedField(many=True)
    actor = serializers.StringRelatedField(many=True)
    stillCut = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'movieCd', 'movieNm', 'openDt', 'audiAcc', 'movieNmEn', 'showTm', 'posterUrl', 'description', 'score', 'trailer', 'genre',  'nation', 'director', 'actor', 'stillCut', 'selected']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'watch']
        
        
class UserWatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'watch']


class ScoreSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Score
        fields = ['id', 'comment', 'score', 'movie', 'user']
