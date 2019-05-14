from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Score

from .forms import ScoreModelForm

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

import json

from .API_CALL.KOFIC.get_daily_list import daily_lists, YESTERDAY


# Create your views here.
def movie_index(request):
    return render(request, 'movies/index.html', {
        'movies': Movie.objects.all(),
        'date': YESTERDAY,
        'daily_lists': json.loads(daily_lists),
    })
  

@login_required
@require_POST
def score_create(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    score_form = ScoreModelForm(request.POST)
    if score_form.is_valid():
        score = score_form.save(commit=False)
        score.movie = movie
        score.user = request.user
        score.save()
    return redirect('movies:movie_index')


@login_required
@require_POST
def score_update(request, movie_id, score_id):
    score = get_object_or_404(Score, pk=score_id)
    if request.method == 'POST':
        score_form = ScoreModelForm(request.POST, instance=score)
        if score_form.is_valid():
            score_form.save()
            return redirect('movies:movie_index')
    else:
        score_form = ScoreModelForm(instance=score)
        return redirect("movies:movie_index") # render 해야 함 or Vue


@login_required
@require_POST
def score_delete(request, movie_id, score_id):
    score = get_object_or_404(Score, pk=score_id)
    score.delete()
    return redirect('movies:movie_index')


def movie_suggestions(request):
    return render(request, 'movies/suggestions.html')


""" REST API
# from django.contrib.auth import get_user_model
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .serializers import ScoreSerializer



@api_view(['GET', 'POST'])
def score_create_read(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
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
"""