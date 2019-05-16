from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Score, Genre, Nation, Director, Actor, StillCut


from datetime import datetime
from .forms import ScoreModelForm

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MovieSerializer, ScoreSerializer, GenreSerializer

from django.http import HttpResponse

# from .API_CALL.KOFIC.get_daily_list import daily_lists, YESTERDAY
# from .API_CALL.KOFIC.get_data import a
# from .API_CALL.KOFIC.organize import a
# from .API_CALL.KOFIC.get_json import a

# Create your views here.
def intro(request):
    return render(request, 'movies/intro.html')


def movie_index(request):
    return render(request, 'movies/index.html', {
        # 'daily_lists': list(Movie.objects.all()),
        'date': int(datetime.today().strftime('%Y%m%d')) - 1,
        'userID': request.user.id,
        # 'date': YESTERDAY,
        # 'daily_lists': daily_lists,
    })

def movie_suggestions(request):
    return render(request, 'movies/suggestions.html')
    

def movie_watchlist(request):
    return render(request, 'movies/watchlist.html')
    

@api_view(['GET'])
def movie_get(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)
    
    
@api_view(['GET'])
def genre_get(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)  


# @api_view(['GET'])
# def watch_get(request, user_id):
#     user = get_object_or_404(get_user_model(), pk=user_id)
#     serializer = UserWatchSerializer(user, many=True)
#     return Response(serializer.data)


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


@api_view(['GET'])
def score_read_only(request):
    scores = Score.objects.all()
    serializer = ScoreSerializer(scores, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def score_create_read(request,movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    if request.method == 'POST':
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie, user=request.user)
            msg_dict = { "message": "작성되었습니다." }
            return Response(msg_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        scores = movie.scores.all()
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)
        

@api_view(['PUT', 'DELETE'])
def score_update_delete(request, score_id):
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
        

def watch_get(request,movie_id):
    # 1. like를 추가할 포스트를 가져옴.
    movie = get_object_or_404(Movie, pk=movie_id)
    # 2. 만약 유저가 해당 post를 이미 like 했다면, like를 제거하고. 아니면, like를 추가한다.
    if request.user in movie.watchUsers.all():
        movie.watchUsers.remove(request.user)
    else:
        movie.watchUsers.add(request.user)
    return HttpResponse('')
    # msg_dict = { "message": "수정되었습니다." }
    # return Response(msg_dict)
