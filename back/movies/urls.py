from django.urls import path
from . import views
from . import main_logic

urlpatterns = [
    # 영화 전체조회
    path('movies/', views.movie_list),

    # 하나의 영화에 대한 세부 정보 조회
    path('movies/<int:movie_pk>/', views.movie_detail),
    
    # 하나의 영화에 대한 리뷰 조회
    path('movies/<int:movie_pk>/reviews/', views.reviews_list),

    # 하나의 영화를 랜덤 조회
    path('movies/random/', views.movie_random_detail),
    
    # 영화 최신 순, 평점 순, 인기 순 선택 조회
    path('movies/sorted/', views.movie_list_sorted),

    path('movies/latest/', views.movie_latest),
    path('movies/popularity/', views.movie_popularity),
    path('movies/vote/', views.movie_vote),

    # 좋아요 기준으로 영화 추천 기능
    path('movies/recommend/like/', views.recommend_like_movies), 

    # 계절을 기준으로 영화 추천 기능
    path('movies/recommend/season/', views.recommend_season), 
    
     # 리뷰 수정,삭제, 조회
    path('reviews/<int:review_pk>/', views.review_detail),

    # 영화 좋아요 기능
    path('movies/<int:movie_pk>/like/', views.like_movie),

    # 배우 조회
    path('actors/', views.actor_list),

    # 배우 좋아요 기능
    path('actors/<int:actor_pk>/like/', views.like_actor),

    # 좋아요한 배우를 기반으로 영화 추천 기능
    path('movies/recommend/actor/', views.recommend_like_actors),
    
    # 영화 검색 기능
    path('movies/search/', views.search_movie),

    # 아이디어 추천 기능
    path('movies/recommend/today/', main_logic.today)
]
