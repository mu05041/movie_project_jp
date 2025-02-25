import json

def convert_genre_ids_to_korean():
    # 장르 ID와 한글 이름 매핑
    genre_mapping = {
        28: "액션",
        12: "모험",
        16: "애니메이션",
        35: "코미디",
        80: "범죄",
        99: "다큐멘터리",
        18: "드라마",
        10751: "가족",
        14: "판타지",
        36: "역사",
        27: "공포",
        10402: "음악",
        9648: "미스터리",
        10749: "로맨스",
        878: "SF",
        10770: "TV 영화",
        53: "스릴러",
        10752: "전쟁",
        37: "서부"
    }

    # 기존 JSON 파일 읽기
    with open("movies/fixtures/movies.json", "r", encoding="utf-8") as f:
        movie_data = json.load(f)

    # 각 영화의 장르 ID를 한글 장르명으로 변환
    for movie in movie_data:
        if "fields" in movie and "genres" in movie["fields"]:
            genre_ids = movie["fields"]["genres"]
            korean_genres = [genre_mapping[genre_id] for genre_id in genre_ids if genre_id in genre_mapping]
            movie["fields"]["genres"] = korean_genres

    # 변환된 데이터를 다시 JSON 파일로 저장
    with open("movies/fixtures/movies.json", "w", encoding="utf-8") as w:
        json.dump(movie_data, w, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    convert_genre_ids_to_korean()
    print("장르 변환이 완료되었습니다!")