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
    string = string.replace(u'\r', u' ')
    
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
    
    if daily['nations'][0]['nationNm'] == '한국':
        youtubeSearchUrl = youtubeSearchBaseUrl + daily["movieNm"] + " " + "예고편"
    else:
        youtubeSearchUrl = youtubeSearchBaseUrl + daily["movieNmEn"] + " " + "trailer"
    
    response = requests.get(youtubeSearchUrl).text
    res = bs(response,'html.parser')
    results = res.find_all('a')
    
    for result in results:
        if '/watch?v=' in result.get('href'):
            return result.get('href')[9:]
            
            
def single_to_double(string):
    string = string.replace("'",'"')
    return string
            
    

# BASE
KOFIC_MOVIE_TOKEN = os.getenv('KOFIC_MOVIE_TOKEN')
YESTERDAY = int(datetime.today().strftime('%Y%m%d')) - 1
NAVER_MOVIE_BASE_URL = 'https://movie.naver.com/movie'



# KOFIC Daily Box Office(DBO)
# DBO_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={KOFIC_MOVIE_TOKEN}&targetDt=20180713'
# DBO_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={KOFIC_MOVIE_TOKEN}&targetDt=20180913'
# DBO_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={KOFIC_MOVIE_TOKEN}&targetDt=20180113'
# DBO_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={KOFIC_MOVIE_TOKEN}&targetDt=20190313'
DBO_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={KOFIC_MOVIE_TOKEN}&targetDt=20190513'
DBO_response = requests.get(DBO_url)
daily_lists = DBO_response.json()['boxOfficeResult']['dailyBoxOfficeList'] # JSON File



for daily in daily_lists:
    # audiAcc 단위수 조절
    # daily['audiAcc'] = insert_comma(daily['audiAcc'])



    # 영화 데이터 추가
    movie_info_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={KOFIC_MOVIE_TOKEN}&movieCd={daily["movieCd"]}'
    movie_info_response = requests.get(movie_info_url).json()["movieInfoResult"]["movieInfo"]
    daily.update(movie_info_response)



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
        "rnum": "1",
        "rank": "1",
        "rankInten": "0",
        "rankOldAndNew": "OLD",
        # "movieCd": "20184889",
        # "movieNm": "어벤져스: 엔드게임",
        # "openDt": "20190424",
        "salesAmt": "738244210",
        "salesShare": "39.8",
        "salesInten": "-1923986000",
        "salesChange": "-72.3",
        "salesAcc": "112507888440",
        "audiCnt": "82379",
        "audiInten": "-208402",
        "audiChange": "-71.7",
        # "audiAcc": "12882040",
        "scrnCnt": "1537",
        "showCnt": "5771",
        # "movieNmEn": "Avengers: Endgame",
        "movieNmOg": "",
        # "showTm": "180",
        "prdtYear": "2018",
        "prdtStatNm": "개봉",
        "typeNm": "장편",
        # "nations": [
        #     {
        #         "nationNm": "미국"
        #     }
        # ],
        # "genres": [
        #     {
        #         "genreNm": "액션"
        #     },
        #     {
        #         "genreNm": "SF"
        #     }
        # ],
        # "directors": [
        #     {
        #         "peopleNm": "안소니 루소",
        #         "peopleNmEn": "Anthony Russo"
        #     },
        #     {
        #         "peopleNm": "조 루소",
        #         "peopleNmEn": "Joe Russo"
        #     }
        # ],
        # "actors": [
        #     {
        #         "peopleNm": "로버트 다우니 주니어",
        #         "peopleNmEn": "Robert Downey Jr.",
        #         "cast": "",
        #         "castEn": ""
        #     },
        #     {
        #         "peopleNm": "크리스 에반스",
        #         "peopleNmEn": "Chris Evans",
        #         "cast": "",
        #         "castEn": ""
        #     },
        #     {
        #         "peopleNm": "마크 러팔로",
        #         "peopleNmEn": "Mark Ruffalo",
        #         "cast": "",
        #         "castEn": ""
        #     },
        #     {
        #         "peopleNm": "크리스 헴스워스",
        #         "peopleNmEn": "Chris Hemsworth",
        #         "cast": "",
        #         "castEn": ""
        #     },
        #     {
        #         "peopleNm": "스칼렛 요한슨",
        #         "peopleNmEn": "Scarlett Johansson",
        #         "cast": "",
        #         "castEn": ""
        #     },
        #     {
        #         "peopleNm": "제레미 레너",
        #         "peopleNmEn": "Jeremy Renner",
        #         "cast": "",
        #         "castEn": ""
        #     },
        #     {
        #         "peopleNm": "돈 치들",
        #         "peopleNmEn": "Don Cheadle",
        #         "cast": "",
        #         "castEn": ""
        #     },
        #     {
        #         "peopleNm": "폴 러드",
        #         "peopleNmEn": "Paul Rudd",
        #         "cast": "",
        #         "castEn": ""
        #     },
        #     {
        #         "peopleNm": "브리 라슨",
        #         "peopleNmEn": "Brie Larson",
        #         "cast": "",
        #         "castEn": ""
        #     },
        #     {
        #         "peopleNm": "카렌 길런",
        #         "peopleNmEn": "Karen Gillan",
        #         "cast": "",
        #         "castEn": ""
        #     },
        #     {
        #         "peopleNm": "브래들리 쿠퍼",
        #         "peopleNmEn": "Bradley Cooper",
        #         "cast": "",
        #         "castEn": ""
        #     },
        #     {
        #         "peopleNm": "조슈 브롤린",
        #         "peopleNmEn": "Josh Brolin",
        #         "cast": "",
        #         "castEn": ""
        #     }
        # ],
        "showTypes": [
            {
                "showTypeGroupNm": "2D",
                "showTypeNm": "디지털"
            },
            {
                "showTypeGroupNm": "3D",
                "showTypeNm": "3D 디지털"
            },
            {
                "showTypeGroupNm": "4D",
                "showTypeNm": "4D"
            },
            {
                "showTypeGroupNm": "IMAX",
                "showTypeNm": "IMAX"
            },
            {
                "showTypeGroupNm": "IMAX",
                "showTypeNm": "IMAX 3D"
            }
        ],
        "companys": [
            {
                "companyCd": "20161801",
                "companyNm": "월트디즈니컴퍼니코리아 유한책임회사",
                "companyNmEn": "The Walt Disney Company Korea",
                "companyPartNm": "배급사"
            },
            {
                "companyCd": "20161801",
                "companyNm": "월트디즈니컴퍼니코리아 유한책임회사",
                "companyNmEn": "The Walt Disney Company Korea",
                "companyPartNm": "수입사"
            }
        ],
        "audits": [
            {
                "auditNo": "2019-MF00676",
                "watchGradeNm": "12세이상관람가"
            },
            {
                "auditNo": "2019-MF00709",
                "watchGradeNm": "12세이상관람가"
            }
        ],
        "staffs": [],
        # "posterUrl": "https: //movie-phinf.pstatic.net/20190417_250/1555465284425i6WQE_JPEG/movie_image.jpg?type=m203_290_2",
        # "description": "인피니티 워 이후 절반만 살아남은 지구 마지막 희망이 된 어벤져스 먼저 떠난 그들을 위해 모든 것을 걸었다!  위대한 어벤져스 운명을 바꿀 최후의 전쟁이 펼쳐진다!",
        # "score": "9.51",
        # "stillCuts": [
        #     "https://movie-phinf.pstatic.net/20190423_104/1555994321040d2AcJ_JPEG/movie_image.jpg?type=m665_443_2",
        #     "https://movie-phinf.pstatic.net/20190423_5/1555994321522brgKj_JPEG/movie_image.jpg?type=m665_443_2",
        #     "https://movie-phinf.pstatic.net/20190423_41/1555994321935RJdum_JPEG/movie_image.jpg?type=m665_443_2"
        # ],
        # "trailer": "TcMBFSGVi1c"
    }
    """

movie_dics = []
movie_genre_dics = []
movie_nation_dics = []
movie_director_dics = []
movie_actor_dics = []
movie_stillCut_dics = []
for i in range(len(daily_lists)):
    genre_lists = []
    nation_lists = []
    director_lists = []
    actor_lists = []
    stillCut_lists = []
    movie = {
        "pk": i + 41,
        "model": "movies.movie",
        "fields": {
            "movieCd": daily_lists[i]["movieCd"],
            "movieNm": daily_lists[i]["movieNm"],
            "openDt": daily_lists[i]["openDt"],
            "audiAcc": daily_lists[i]["audiAcc"],
            "movieNmEn": daily_lists[i]["movieNmEn"],
            "showTm": daily_lists[i]["showTm"],
            "posterUrl": daily_lists[i]["posterUrl"],
            "description": daily_lists[i]["description"],
            "score": daily_lists[i]["score"],
            "trailer": daily_lists[i]["trailer"]
        }
    }
    movie_dics.append(movie)
    
    for j in range(len(daily_lists[i]["genres"])):
        genre = daily_lists[i]["genres"][j]["genreNm"]
        if genre not in genre_lists:
            genre_lists.append(genre)
    movie_genre_dics.append(genre_lists)
    
    for k in range(len(daily_lists[i]["nations"])):
        nation = daily_lists[i]["nations"][k]["nationNm"]
        if nation not in nation_lists:
            nation_lists.append(nation)
    movie_nation_dics.append(nation_lists)
            
    for x in range(len(daily_lists[i]["directors"])):
        director = daily_lists[i]["directors"][x]["peopleNm"]
        if director not in director_lists:
            director_lists.append(director)
    movie_director_dics.append(director_lists)
            
    for y in range(len(daily_lists[i]["actors"])):
        actor = daily_lists[i]["actors"][y]["peopleNm"]
        if actor not in actor_lists:
            actor_lists.append(actor)
    movie_actor_dics.append(actor_lists)
        
    for z in range(len(daily_lists[i]["stillCuts"])):
        stillCut = daily_lists[i]["stillCuts"][z]
        stillCut_lists.append(stillCut)    
    movie_stillCut_dics.append(stillCut_lists)
    
        
print(movie_dics,end="\n")
print(movie_genre_dics,end="\n")
print(movie_nation_dics,end="\n")
print(movie_director_dics,end="\n")
print(movie_actor_dics,end="\n")
print(movie_stillCut_dics,end="\n")


# print(list(enumerate(movie_genre_dics, 41)),end='\n')
# print(list(enumerate(movie_nation_dics, 41)),end='\n')
# print(list(enumerate(movie_director_dics, 41)),end='\n')
# print(list(enumerate(movie_actor_dics, 41)),end='\n')
# print(list(enumerate(movie_stillCut_dics, 41)),end='\n')