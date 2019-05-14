from django.shortcuts import render, get_object_or_404
from .models import Movie, Score

from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ScoreSerializer

from .forms import ScoreModelForm

from .API_CALL.KOFIC.get_daily_list import daily_lists, YESTERDAY
# from pprint import pprint


# Create your views here.
def movie_index(request):
    return render(request, 'movies/index.html', {
        'date': YESTERDAY,
        'daily_lists': daily_lists,
        'form': ScoreModelForm()
    })
  
def movie_suggestions(request):
    return render(request, 'movies/suggestions.html')
  
    
@api_view(['GET', 'POST'])
def score_create_read(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=get_user_model())
            msg_dict = { "message": "작성되었습니다." }
            return Response(msg_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        scores = movie.scores.all()
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)
        


@api_view(['PUT', 'DELETE'])
def score_update_delete(request, movie_id, score_id):
    score = get_object_or_404(Score, pk=score_id)
    if request.method == 'PUT':
        serializer = ScoreSerializer(score, data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg_dict = { "message": "수정되었습니다." }
            return Response(msg_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        score.delete()
        msg_dict = { "message": "삭제되었습니다." }
        return Response(msg_dict)