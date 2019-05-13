import requests
import os
from bs4 import BeautifulSoup as bs
from datetime import datetime
import json

def insert_comma(n):
    # 음수일 경우를 고려
    if n[0] == '-':
        return '-' + insert_comma(n[1:])
    if len(n) <= 3:
        return n
    if n.find('.') == -1:
        return insert_comma(n[:-3]) + ',' + n[-3:]
    else:
        return insert_comma(n[:n.find('.')]) + n[n.find('.'):]

# BASE_KOFIC
KOFIC_MOVIE_TOKEN = os.getenv('KOFIC_MOVIE_TOKEN')
YESTERDAY = int(datetime.today().strftime('%Y%m%d')) - 1

# KOFIC 일일 박스 오피스(하루 전으로 데이터 받음)
daily_box_office_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={KOFIC_MOVIE_TOKEN}&targetDt={YESTERDAY}'
daily_response = requests.get(daily_box_office_url)
daily_lists = daily_response.json()['boxOfficeResult']['dailyBoxOfficeList'] # JSON File


# 후처리
NAVER_MOVIE_BASE_URL = 'https://movie.naver.com/movie'
for daily in daily_lists:
    
    name = daily['movieNm']
    SEARCH_BASE_URL = f'https://movie.naver.com/movie/search/result.nhn?query={name}&section=all&ie=utf8'
    response = requests.get(SEARCH_BASE_URL).text
    res = bs(response, 'html.parser')
    result = res.select_one('#old_content > ul.search_list_1 > li > dl > dt > a').get('href')
    
    URL = f'{NAVER_MOVIE_BASE_URL}{result}'
    sub_photo_URL = URL.replace('basic','photoView')
    
    response = requests.get(URL).text
    
    res = bs(response,'html.parser')
    
    # 결과들
    poster_result = res.select_one('#content > div.article > div.mv_info_area > div.poster > a > img').get('src')
    idx = poster_result.find('?')
    
    description_result = res.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p').text
    
    score_result = res.select_one('#actualPointPersentBasic > div > span > span')
    if score_result == None:
        score_result = 0
    else:
        score_result = score_result.text[7:-1]
    
    
    # 스틸컷 저장
    tmp1 = requests.get(sub_photo_URL).text
    tmp2 = bs(tmp1, 'html.parser')
    for i in range(1,4):
        sub_photo_result = tmp2.select_one(f'#photo_area > div > div.list_area._list_area > div > ul > li:nth-child({i})').get('data-json')
        # 74, 665, 886
        tmp3 = json.loads(sub_photo_result)['fullImageUrl665px']
        name = f'subPhoto{i}'
        daily[name] = tmp3
    
    
    # image 저장
    # Thumbnail image
    daily['poster_url'] = poster_result
    # Original image
    # daily['poster_url'] = poster_result[:idx]
    
    # audiAcc 단위수 조절
    daily['audiAcc'] = insert_comma(daily['audiAcc'])
    
    # 줄거리 저장
    daily['description'] = description_result
    
    # 평균평점 저장
    daily['score'] = score_result
    
    # 영화 영어이름 저장
    movie_info_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={KOFIC_MOVIE_TOKEN}&movieCd={daily["movieCd"]}'
    movie_info_response = requests.get(movie_info_url).json()
    daily["movieNmEn"] = movie_info_response["movieInfoResult"]["movieInfo"]["movieNmEn"]
    
    # 유튜브에서 트레일러 ID 가져오기
    youtubeSearchBaseUrl = "https://www.youtube.com/results?search_query="
    
    if movie_info_response["movieInfoResult"]["movieInfo"]['nations'][0]['nationNm'] == '한국':
        youtubeSearchUrl = youtubeSearchBaseUrl + daily["movieNm"] + " " + "예고편"
    else:
        youtubeSearchUrl = youtubeSearchBaseUrl + daily["movieNmEn"] + " " + "trailer"
    
    response = requests.get(youtubeSearchUrl).text
    res = bs(response,'html.parser')
    results = res.find_all('a')
    
    for result in results:
        if '/watch?v=' in result.get('href'):
            # daily['trailer'] = 'https://www.youtube.com' + result.get('href')
            daily['trailer'] = result.get('href')[9:]
            break