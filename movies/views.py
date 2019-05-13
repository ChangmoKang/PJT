from django.shortcuts import render
from .API_CALL.KOFIC.get_daily_list import daily_lists, YESTERDAY
from pprint import pprint


# # DATA 예시
# example = "http://open.kmrb.or.kr/openapi-data/service/MvResultService/mvResult?ServiceKey=eoAkRfyhoJHQEabBvocVCyqtia7SXnDgxHcuyYVAwkmeqcGIWnYGm51eksFbXWe467lzAfsesG3Dihb9tLc%2FQQ%3D%3D&pageNo=1&numOfRows=1&title=%EC%96%B4%EB%B2%A4%EC%A0%B8%EC%8A%A4:%20%EC%97%94%EB%93%9C%EA%B2%8C%EC%9E%84"
# data_api = "eoAkRfyhoJHQEabBvocVCyqtia7SXnDgxHcuyYVAwkmeqcGIWnYGm51eksFbXWe467lzAfsesG3Dihb9tLc%2FQQ%3D%3D"

# Create your views here.
def movie_index(request):
    return render(request, 'movies/index.html', {
        'date': YESTERDAY,
        'daily_lists': daily_lists,
    })
    
    