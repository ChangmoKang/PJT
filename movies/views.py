from django.shortcuts import render
from .API_CALL.KOFIC.get_daily_list import daily_lists, YESTERDAY
# from pprint import pprint


# Create your views here.
def movie_index(request):
    return render(request, 'movies/index.html', {
        'date': YESTERDAY,
        'daily_lists': daily_lists,
    })
    
    