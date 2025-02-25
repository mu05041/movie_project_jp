from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # 특정 유저의 리뷰 목록 조회
    path('<int:user_pk>/reviews/', views.user_reviews, name='user_reviews'),

    # 프로필 정보 조회
    path('<int:user_pk>/', views.profile, name='profile'),

    # 팔로우 기능
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    
     # 프로필 내부에서 내가 좋아요한 영화 조회하기
    path('<int:user_pk>/liked-movies/', views.user_liked_movies, name='user_liked_movies'),

    # 프로필 내부에서 내가 좋아요한 배우 조회하기
    path('<int:user_pk>/liked-actors/', views.user_liked_actors, name='user_liked_actors'),

]
