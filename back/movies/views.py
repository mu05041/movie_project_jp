from rest_framework.response import Response
from rest_framework.decorators import api_view
import heapq, math, random

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import MovieListSerializer, MovieSerializer
from .serializers import ReviewListSerializer, ReviewSerializer
from .serializers import MovieSearchSerializer, ActorSerializer
from .serializers import TodaySerializer
from .models import Movie, Review, Actor, Recommended
from django.contrib.auth import get_user_model

from collections import Counter
from django.db.models import Q
from datetime import datetime
from difflib import SequenceMatcher


# 영화 전체 목록 조회
@api_view(['GET'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.order_by('?')[:12]
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

# 한 영화에 대한 세부 정보 조회
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
# 랜덤으로 한 영화를 추천
# 한 영화에 대한 세부 정보 조회
@api_view(['GET'])
def movie_random_detail(request, movie_pk=None):
    # movie_pk가 없으면 랜덤으로 선택
    if movie_pk is None:
        movie_count = Movie.objects.count()
        if movie_count == 0:
            return Response({"error": "No movies available."}, status=404)
        random_index = random.randint(0, movie_count - 1)
        movie = Movie.objects.all()[random_index]
    else:
        movie = get_object_or_404(Movie, pk=movie_pk)

    serializer = MovieSerializer(movie)
    return Response(serializer.data)


# 영화 조회를 최신순 인기순 평점순 정렬
@api_view(['GET'])
def movie_list_sorted(request):
    today = datetime.now().date()  # 현재 날짜
    # 기본 정렬 기준을 최신순으로 설정
    order_by = request.GET.get('order_by', 'latest')

    # 정렬 기준에 따라 쿼리셋 변경
    if order_by == 'latest':
        # 오늘 이전에 개봉한 영화만 포함
        movies = Movie.objects.filter(release_date__lte=today).order_by('-release_date')[:30]
    elif order_by == 'vote_average':
        movies = Movie.objects.order_by('-vote_average')[:30]  # 평점순
    elif order_by == 'popularity':
        movies = Movie.objects.order_by('-popularity')[:30]  # 인기순
    else:
        return Response({'error': 'Invalid order_by parameter'}, status=400)

    # 시리얼라이저를 사용하여 데이터 직렬화
    serializer = MovieListSerializer(movies, many=True)

    # JSON 응답 반환
    return Response(serializer.data)


@api_view(['GET'])
def movie_latest(request):
    today = datetime.now().date()  # 현재 날짜
    # 오늘 이전에 개봉한 영화만 포함
    movies = Movie.objects.filter(release_date__lte=today).order_by('-release_date')[:30]
    # 시리얼라이저를 사용하여 데이터 직렬화
    serializer = MovieListSerializer(movies, many=True)

    # JSON 응답 반환
    return Response(serializer.data)


@api_view(['GET'])
def movie_popularity(request):
    movies = Movie.objects.order_by('-popularity')[:30]  # 인기순
    # 시리얼라이저를 사용하여 데이터 직렬화
    serializer = MovieListSerializer(movies, many=True)
    # JSON 응답 반환
    return Response(serializer.data)


@api_view(['GET'])
def movie_vote(request):
    movies = Movie.objects.order_by('-vote_average')[:30]  # 평점순
    # 시리얼라이저를 사용하여 데이터 직렬화
    serializer = MovieListSerializer(movies, many=True)
    # JSON 응답 반환
    return Response(serializer.data)


# 리뷰 조회와 작성
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def reviews_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    if request.method == 'GET':
        # 영화에 대한 리뷰 전체 조회
        reviews = movie.reviews.all().order_by('-created_at')
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(f"movie: {movie}, user: {request.user}")  # 로그 확인
            
            # serializer.save()로 movie와 user 정보를 추가
            serializer.save(movie=movie, user=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 리뷰 수정 및 삭제, 조회
@api_view(['GET', 'DELETE', 'PUT'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    # 리뷰 작성자만 수정 및 삭제 가능
    if request.method in ['DELETE', 'PUT'] and review.user != request.user:
        raise PermissionDenied("권한이 없습니다.")  # 예외 발생
    
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


# 영화 좋아요 기능
@api_view(['POST'])
def like_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    # 사용자가 이미 좋아요를 눌렀는지 확인
    if request.user in movie.like_users.all():
        movie.like_users.remove(request.user)
        is_liked = False
    else:
        movie.like_users.add(request.user)
        is_liked = True
    
    # 응답 데이터
    context = {
        'is_liked' : is_liked,
        'like_count' : movie.like_users.count(),

    }
    return Response(context)


# 배우 조회
@api_view(['GET'])
def actor_list(request):
    actors = get_list_or_404(Actor)
    serializer = ActorSerializer(actors, many=True)
    return Response(serializer.data)


# 배우 좋아요 기능 
@api_view(['POST'])
def like_actor(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)

    # 사용자가 이미 좋아요한 배우인지 확인
    if request.user in actor.like_users.all():
        actor.like_users.remove(request.user)
        is_liked = False
    else:
        actor.like_users.add(request.user)
        is_liked = True
    
    # 응답 데이터
    context = {
        'is_liked' : is_liked,
        'like_count' : actor.like_users.count(),
    }
    return Response(context)


# 영화 좋아요 기반 영화 추천
@api_view(['GET'])
def recommend_like_movies(request):
    # 인증된 사용자만 접근 가능
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=401)
    
    # 사용자가 좋아요를 누른 영화들을 가져옴
    liked_movies = request.user.like_movies.all()
    
    # 사용자가 좋아한 영화들의 장르 추출
    liked_genres = liked_movies.values_list('genres', flat=True)
    
    # 장르별 비율 계산
    genre_count = Counter(liked_genres)
    total_genres = len(liked_genres)
    
    # 각 장르의 비율 계산 (0과 나누는 에러 방지)
    genre_ratio = {genre: count / total_genres for genre, count in genre_count.items()}
    
    # 추천 영화들을 담을 리스트
    recommended_movies = []
    
    # 장르 비율에 맞춰 추천 영화 추출
    for genre, ratio in genre_ratio.items():
        # 장르에 맞는 영화를 찾고, 사용자가 아직 좋아요를 누르지 않은 영화를 필터링
        genre_movies = Movie.objects.filter(genres=genre).exclude(like_users=request.user)
        
        # 추천할 영화 수를 비율에 맞춰 결정 (최대 15개 추천)
        num_recommended = int(ratio * 15)
        num_recommended = max(num_recommended, 3)  # 최소 1개 영화는 추천
        
         # 무작위로 선택 (단, 영화 수가 부족할 경우 최대 가능한 수만 선택)
        genre_movies = list(genre_movies)
        if genre_movies:
            sampled_movies = random.sample(genre_movies, min(len(genre_movies), num_recommended))
            recommended_movies.extend(sampled_movies)
    
    # 추천 영화들을 직렬화
    recommended_movies = list(set(recommended_movies))  # 중복 제거
    recommended_movies = random.sample(recommended_movies, min(len(recommended_movies), 15))  # 최종적으로 15개 무작위 선택
    
    # 직렬화
    serializer = MovieSerializer(recommended_movies, many=True)
    return Response(serializer.data)


# 배우 좋아요 기반 배우의 다른 영화 추천 기능 
@api_view(['GET'])
def recommend_like_actors(request):
      # 인증된 사용자만 접근 가능
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=401)
    
    # 사용자가 좋아요를 배우들을 가져옴
    liked_actors = request.user.like_actors.all()
    
    # 추천할 영화들을 담을 리스트
    recommended_movies = []
    
    # 사용자가 좋아요한 배우들의 다른 영화들을 추천
    for actor in liked_actors:
        # 해당 배우가 출연한 영화들 가져오기
        actor_movies = Movie.objects.filter(actors=actor).exclude(like_users=request.user)
        
        # 추천할 영화들을 비율에 맞춰 추출 (최대 15개 추천)
        num_recommended = min(len(actor_movies), 3)  # 최소 1개 영화는 추천
        
        # 무작위로 선택 (단, 영화 수가 부족할 경우 최대 가능한 수만 선택)
        actor_movies = list(actor_movies)
        if actor_movies:
            sampled_movies = random.sample(actor_movies, num_recommended)
            recommended_movies.extend(sampled_movies)
    
    # 추천 영화들을 직렬화
    recommended_movies = list(set(recommended_movies))  # 중복 제거
    recommended_movies = random.sample(recommended_movies, min(len(recommended_movies), 15))  # 최종적으로 15개 무작위 선택
    
    # 직렬화
    serializer = MovieSerializer(recommended_movies, many=True)
    return Response(serializer.data)


# 계절에 따른 영화 추천 기능
def get_season():
    month = datetime.now().month
    if 3 <= month <= 5:
        return "봄"  # 봄
    elif 6 <= month <= 8:
        return "여름"  # 여름
    elif 9 <= month <= 11:
        return "가을"  # 가을
    else:
        return "겨울"  # 겨울

def get_seasonal_genre(season):
    seasonal_genres = {
        "spring": ["로맨스", "드라마"],
        "summer": ["액션", "모험", "스릴러", "코미디"],
        "autumn": ["미스터리", "SF", "드라마", "스릴러", "역사"],
        "winter": ["코미디", "로맨스", "가족", "애니메이션"]
    }
    return seasonal_genres.get(season, [])

@api_view(['GET'])
def recommend_season(request):
    # 현재 계절을 가져옴
    season = get_season()
    # 계절에 맞는 영화 장르 목록을 가져옴
    genres = get_seasonal_genre(season)

    # Q 객체를 사용하여 여러 장르에 대해 OR 조건을 생성
    q = Q()
    for genre in genres:
        q |= Q(genres__contains=genre)
    
    # 영화 필터링: 계절에 맞는 장르가 하나라도 포함된 영화들만 필터링
    recommended_movies = list(Movie.objects.filter(q))
    
    # 랜덤으로 15개의 영화를 선택 (단, 영화 데이터가 15개 미만일 경우 모든 영화 반환)
    recommended_movies = random.sample(recommended_movies, min(len(recommended_movies), 15))

    # MovieSerializer와 연관해서 필터링
    serializer = MovieSerializer(recommended_movies, many=True)
    
    # 계절 정보와 추천된 영화 목록을 반환
    return Response({
        'season': season,
        'recommended_movies': serializer.data
    })


# 영화 검색 기능
def similarity_score(a, b):
    """Calculate similarity score between two strings."""
    return SequenceMatcher(None, a, b).ratio()


@api_view(['GET'])
def search_movie(request):
    query = request.GET.get('search', '').strip()  # 쿼리 파라미터에서 검색어 가져오기
    if not query:  # 검색어가 없거나 빈 문자열인 경우
        return Response(
            {"message": "검색어를 입력해주세요."},
            status=400  # Bad Request
        )

    # 제목 또는 개요에서 검색
    movies = Movie.objects.filter(Q(title__icontains=query) | Q(overview__icontains=query))
    if not movies.exists():  # 검색 결과가 없는 경우
        return Response(
            {"message": f"'{query}'에 대한 검색 결과가 없습니다."},
            status=404  # Not Found
        )

    # 중복 제거 (중복 영화를 제거)
    unique_movies = {movie.id: movie for movie in movies}.values()

    # 유사도 계산 및 정렬
    movies_with_similarity = []
    for movie in unique_movies:
        similarity = similarity_score(query.lower(), movie.title.lower())
        movie.similarity = similarity  # `MovieSearchSerializer`의 `similarity` 필드 사용
        movies_with_similarity.append(movie)

    # 유사도 기준으로 정렬
    sorted_movies = sorted(movies_with_similarity, key=lambda x: x.similarity, reverse=True)[:15]

    # 직렬화 및 응답 반환
    serializer = MovieSearchSerializer(sorted_movies, many=True)
    return Response(serializer.data)