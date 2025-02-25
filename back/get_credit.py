import requests
import json

TMDB_API_KEY = '39bbf7a1577f75074bd46739a98865cd'

def get_movie_datas():
    total_data = []
    print('11111')
    for i in range(1, 51):
        request_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page={i}"
        movies = requests.get(request_url).json()
        for movie in movies['results']:
            tmp_id = movie['id']
            if movie.get('release_date', ''):
                fields = {
                    # 'movie_id': movie['id'],
                    'title': movie['title'],
                    'release_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'vote_average': movie['vote_average'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'backdrop_path': movie['backdrop_path'],
                    'genres': movie['genre_ids']
                }

            print(tmp_id)
            
            ## 영화 감독 및 배우정보
            creadit_url =f"https://api.themoviedb.org/3/movie/{tmp_id}/credits?api_key={TMDB_API_KEY}&language=ko-KR"

            credits = requests.get(creadit_url).json()
            credit_flag = True # 배우, 감독 정보가 없는 영화일 경우 필터링하기
            actors = []
            actor_datas = []
            for actor in credits['cast'][:3]:

                actor_id = actor["id"]
                actors.append(actor_id)

                actor_name = actor["name"]
                actor_popularity = actor["popularity"]
                actor_profile_path = actor["profile_path"]

                if actor_name == "" or actor_popularity == 0 or actor_profile_path == None: # 필터링
                    credit_flag = False
                    break
                
                # 배우 DB
                actor_data = {
                    "model": "movies.actor",
                    "pk": actor_id,
                    "fields": {
                        'name': actor_name,
                        'popularity': actor_popularity,
                        'profile_path': actor_profile_path,
                    }
                }
                actor_datas.append(actor_data)

            if actor_datas:  # 배우 정보가 있는 경우만 데이터 추가
                data = {
                        "pk": movie['id'],
                        "model": "movies.movie",
                        "fields": fields,
                        'actors': actor_datas, 
                    }
                total_data.append(data)

              



    with open("movies/fixtures/movie_credit_data.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=4, ensure_ascii=False)



get_movie_datas()

'''
movies/fixtures/ 만들고 

python init.py 

python manage.py migrate

python manage.py loaddata genre_data.json movie_data.json

json데이터 만든 후 gernew_mapping.py로 장르 다시 매핑해야함

'''