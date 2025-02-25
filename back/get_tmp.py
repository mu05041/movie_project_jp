import requests 
import json

TMDB_API_KEY = '39bbf7a1577f75074bd46739a98865cd'

def get_movie_datas():
    total_data = []
    actor_data_set = []  # 중복 없는 배우 데이터 저장용
    processed_actors = set()  # 이미 처리된 배우 ID 추적
    
    print('11111')
    for i in range(1, 51):
        request_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page={i}"
        movies = requests.get(request_url).json()
        
        for movie in movies['results']:
            tmp_id = movie['id']
            print(tmp_id)
            
            ## 영화 감독 및 배우정보
            creadit_url = f"https://api.themoviedb.org/3/movie/{tmp_id}/credits?api_key={TMDB_API_KEY}&language=ko-KR"
            credits = requests.get(creadit_url).json()
            actor_ids = []  # 배우 ID만 저장
            
            for actor in credits['cast'][:6]:
                actor_id = actor["id"]
                actor_ids.append(actor_id)  # ID만 추가
                
                # 아직 처리되지 않은 배우만 배우 데이터셋에 추가
                if actor_id not in processed_actors:
                    actor_data = {
                        "model": "movies.actor",
                        "pk": actor_id,
                        "fields": {
                            'name': actor["name"],
                            'popularity': actor["popularity"],
                            'profile_path': actor["profile_path"],
                        }
                    }
                    actor_data_set.append(actor_data)
                    processed_actors.add(actor_id)
            
            if movie.get('release_date', '') and actor_ids:  # 배우 정보가 있는 경우만
                movie_data = {
                    'title': movie['title'],
                    'release_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'vote_average': movie['vote_average'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'backdrop_path': movie['backdrop_path'],
                    'genres': movie['genre_ids'],
                    'actors': actor_ids,  # 배우 ID 리스트만 저장
                }
                
                data = {
                    "pk": movie['id'],
                    "model": "movies.movie",
                    "fields": movie_data,
                }
                total_data.append(data)
    
    # 영화 데이터와 배우 데이터를 별도의 파일로 저장
    with open("movies/fixtures/movies.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=4, ensure_ascii=False)
        
    with open("movies/fixtures/actors.json", "w", encoding="utf-8") as w:
        json.dump(actor_data_set, w, indent=4, ensure_ascii=False)

get_movie_datas()