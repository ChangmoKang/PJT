from rest_framework import serializers
from .models import Genre, Nation, Director, Actor, StillCut, Movie, Score


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
    # genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    # nation = serializers.PrimaryKeyRelatedField(queryset=Nation.objects.all(), many=True)
    # director = serializers.PrimaryKeyRelatedField(queryset=Director.objects.all(), many=True)
    # actor = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all(), many=True)
    # stillCut = serializers.PrimaryKeyRelatedField(queryset=StillCut.objects.all(), many=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'movieCd', 'movieNm', 'openDt', 'audiAcc', 'movieNmEn', 'showTm', 'posterUrl', 'description', 'score', 'trailer', 'genre',  'nation', 'director', 'actor', 'stillCut', 'selected']


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['comment', 'score', 'movieCd',]


# class ScoreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Score
#         fields = ['comment', 'score', 'movie', 'user']