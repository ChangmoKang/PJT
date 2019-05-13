import requests
import os
import json

from bs4 import BeautifulSoup as bs
from datetime import datetime


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


def beautify(url, selector):
    response = requests.get(url).text
    bs_response = bs(response, 'html.parser')
    result = bs_response.select_one(selector)
    return result
    
    
def trimming(string):
    string = string.replace(u'\xa0', u' ')
    return string


def get_score_or_0(score):
    if score == None:
        return 0
    else:
        return score.text[7:-1]


def save_data(name, data):
    daily[name] = data


def get_trailer():
    youtubeSearchBaseUrl = "https://www.youtube.com/results?search_query="
    
    if daily["nationNm"] == '한국':
        youtubeSearchUrl = youtubeSearchBaseUrl + daily["movieNm"] + " " + "예고편"
    else:
        youtubeSearchUrl = youtubeSearchBaseUrl + daily["movieNmEn"] + " " + "trailer"
    
    response = requests.get(youtubeSearchUrl).text
    res = bs(response,'html.parser')
    results = res.find_all('a')
    
    for result in results:
        if '/watch?v=' in result.get('href'):
            return result.get('href')[9:]
            
    


# BASE
KOFIC_MOVIE_TOKEN = os.getenv('KOFIC_MOVIE_TOKEN')
YESTERDAY = int(datetime.today().strftime('%Y%m%d')) - 1
NAVER_MOVIE_BASE_URL = 'https://movie.naver.com/movie'


# KOFIC Daily Box Office(DBO)
DBO_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={KOFIC_MOVIE_TOKEN}&targetDt={YESTERDAY}'
DBO_response = requests.get(DBO_url)
daily_lists = DBO_response.json()['boxOfficeResult']['dailyBoxOfficeList'] # JSON File



for daily in daily_lists:
    # audiAcc 단위수 조절
    daily['audiAcc'] = insert_comma(daily['audiAcc'])



    # 영화 영어이름 & 개봉 국가 저장
    movie_info_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={KOFIC_MOVIE_TOKEN}&movieCd={daily["movieCd"]}'
    movie_info_response = requests.get(movie_info_url).json()
    daily["movieNmEn"] = movie_info_response["movieInfoResult"]["movieInfo"]["movieNmEn"]
    daily["nationNm"] = movie_info_response["movieInfoResult"]["movieInfo"]['nations'][0]['nationNm']



    # 영화 URL 뒷 부분 찾기
    """ 
    ex.
    NAVER_MOVIE_BASE_URL 뒤에 "/movie/bi/mi/basic.nhn?code=136900"(어벤져스: 엔드게임)를 찾기 위한 코드.
    """
    SEARCH_BASE_url = f'{NAVER_MOVIE_BASE_URL}/search/result.nhn?query={daily["movieNm"]}&section=all&ie=utf8'
    SEARCH_BASE_selector = '#old_content > ul.search_list_1 > li > dl > dt > a'
    SEARCH_BASE_result = beautify(SEARCH_BASE_url, SEARCH_BASE_selector).get('href')



    # 찾은 영화에서 데이터 추출(basic)
    SEARCH_BASIC_url = f'{NAVER_MOVIE_BASE_URL}{SEARCH_BASE_result}'
    SEARCH_BASIC_selector_posterUrl = '#content > div.article > div.mv_info_area > div.poster > a > img'
    SEARCH_BASIC_selector_description = '#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p'
    SEARCH_BASIC_selector_score = '#actualPointPersentBasic > div > span > span'

    posterUrl = beautify(SEARCH_BASIC_url, SEARCH_BASIC_selector_posterUrl).get('src')
    description = trimming(beautify(SEARCH_BASIC_url, SEARCH_BASIC_selector_description).text)
    score = get_score_or_0(beautify(SEARCH_BASIC_url, SEARCH_BASIC_selector_score))

    save_data("posterUrl", posterUrl)
    save_data("description", description)
    save_data("score", score)



    # 찾은 영화에서 데이터 추출(photoView)
    SEARCH_PHOTOVIEW_stillCut = SEARCH_BASIC_url.replace('basic','photoView')
    
    stillCuts = []
    for i in range(1,4):
        SEARCH_PHOTOVIEW_selector_stillCut = f'#photo_area > div > div.list_area._list_area > div > ul > li:nth-child({i})'
        stillCut = json.loads(beautify(SEARCH_PHOTOVIEW_stillCut,SEARCH_PHOTOVIEW_selector_stillCut).get('data-json'))['fullImageUrl665px']
        stillCuts.append(stillCut)
    save_data("stillCuts", stillCuts)



    # Youtube에서 트레일러 ID 가져오기
    trailer = get_trailer()
    save_data('trailer', trailer)



    # daily 결과 값 예시
    """
    ex. daily
    {
        'audiAcc': '12,799,661',
        'audiChange': '-17.9',
        'audiCnt': '290781',
        'audiInten': '-63447',
        'description': '인피니티 워 이후 절반만 살아남은 지구 마지막 희망이 된 어벤져스 먼저 떠난 그들을 위해 모든 것을 걸었다!  위대한 어벤져스 운명을 바꿀 최후의 전쟁이 펼쳐진다!',
        'movieCd': '20184889',
        'movieNm': '어벤져스: 엔드게임',
        'movieNmEn': 'Avengers: Endgame',
        'nationNm': '미국',
        'openDt': '2019-04-24',
        'posterUrl': 'https://movie-phinf.pstatic.net/20190417_250/1555465284425i6WQE_JPEG/movie_image.jpg?type=m203_290_2',
        'rank': '1',
        'rankInten': '0',
        'rankOldAndNew': 'OLD',
        'rnum': '1',
        'salesAcc': '111769644230',
        'salesAmt': '2662230210',
        'salesChange': '-18.5',
        'salesInten': '-604141240',
        'salesShare': '40.7',
        'score': '9.51',
        'scrnCnt': '1665',
        'showCnt': '6308',
        'stillCuts': ['https://movie-phinf.pstatic.net/20190423_104/1555994321040d2AcJ_JPEG/movie_image.jpg?type=m665_443_2',
                    'https://movie-phinf.pstatic.net/20190423_5/1555994321522brgKj_JPEG/movie_image.jpg?type=m665_443_2',
                    'https://movie-phinf.pstatic.net/20190423_41/1555994321935RJdum_JPEG/movie_image.jpg?type=m665_443_2'],
        'trailer': 'TcMBFSGVi1c'
    }
    """