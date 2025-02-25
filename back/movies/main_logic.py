from rest_framework.response import Response
from rest_framework.decorators import api_view
import random
from collections import defaultdict
from .serializers import MovieSerializer, TodaySerializer
from .models import Movie, Recommended
from rest_framework import status
from django.db.models import Q


@api_view(['GET', 'POST'])
def today(request):
    if request.method == 'GET':
        recommended = Recommended.objects.all()
        serializer = TodaySerializer(recommended, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TodaySerializer(data=request.data)
        print("Received POST request with data:", request.data)
        
        # 감정, 날씨, 음식 정보 저장 및 장르 추천 로직
        if serializer.is_valid(raise_exception=True):
            emotion = serializer.validated_data['emotion']
            weather = serializer.validated_data['weather']
            food = serializer.validated_data['food']
            
            # 기본 장르 추천 기준 설정
            genre_scores = defaultdict(int)
            genres = []

            # 기분에 따른 장르 점수 추가
            if emotion > 70:
                genre_scores['액션'] += 30
                genre_scores['코미디'] += 30
                genre_scores['애니메이션'] += 20
                genres.extend(['액션', '코미디', '애니메이션'])
            elif emotion < 30:
                genre_scores['코미디'] += 20
                genre_scores['다큐멘터리'] += 40
                genre_scores['음악'] += 30
                genres.extend(['코미디', '다큐멘터리', '음악'])
            else:
                genre_scores['스릴러'] += 20
                genre_scores['미스터리'] += 20
                genre_scores['로맨스'] += 20
                genres.extend(['스릴러', '미스터리', '로맨스'])

            # 날씨에 따른 장르 점수 추가
            if weather == '맑음':
                genre_scores['액션'] += 20
                genre_scores['모험'] += 20
                genres.extend(['액션', '모험'])
            elif weather == '비':
                genre_scores['스릴러'] += 30
                genre_scores['미스터리'] += 20
                genre_scores['SF'] += 20
                genre_scores['공포'] += 20
                genres.extend(['스릴러', '미스터리', 'SF', '공포'])
            elif weather == '흐림':
                genre_scores['판타지'] += 20
                genre_scores['전쟁'] += 30
                genre_scores['범죄'] += 30
                genres.extend(['판타지', '전쟁', '범죄'])
            elif weather == '눈':
                genre_scores['음악'] += 20
                genre_scores['가족'] += 30
                genre_scores['역사'] += 20
                genres.extend(['음악', '가족', '역사'])
            
            # 음식에 따른 장르 점수 추가
            if food == '젤리':  # 젤리
                genre_scores['드라마'] += 20
                genre_scores['액션'] += 30
                genres.extend(['드라마', '액션'])
            elif food == '초콜릿':  # 초콜릿
                genre_scores['로맨스'] += 20
                genre_scores['멜로'] += 30
                genres.extend(['멜로', '로맨스'])
            elif food == '과자':  # 과자
                genre_scores['애니메이션'] += 25
                genre_scores['가족'] += 40
                genre_scores['다큐멘터리'] += 30
                genre_scores['역사'] += 20
                genres.extend(['애니메이션', '가족', '다큐멘터리', '역사'])
            elif food == '사탕':  # 사탕
                genre_scores['모험'] += 30
                genre_scores['판타지'] += 20
                genre_scores['스릴러'] += 20
                genres.extend(['모험', '판타지', '스릴러'])


            # 장르 점수 높은 순으로 정렬 후 상위 3개의 장르 선택
            sorted_genres = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)
            genres = [genre for genre, score in sorted_genres[:3]]
            print("Final genres:", genres)  

            # 장르 점수 비율 계산
            total_score = sum(genre_scores.values())
            if total_score == 0:
                return Response({"detail": "No valid genre scores."}, status=status.HTTP_400_BAD_REQUEST)

            # Q 객체를 사용하여 여러 장르에 대해 OR 조건을 생성
            q = Q()
            for genre in genres:
                q |= Q(genres__contains=genre)

            # 필터링된 영화들을 랜덤으로 15개 추천
            recommended_movies = Movie.objects.filter(q)

            # 추천된 영화가 12개 이상일 경우 랜덤으로 12개 선택 (영화가 12개 미만일 경우 모두 반환)
            recommended_movies = random.sample(list(recommended_movies), min(len(recommended_movies), 12))

            # 추천된 영화들 직렬화
            movie_serializer = MovieSerializer(recommended_movies, many=True)

            # 추천 정보를 DB에 저장
            recommended_instance = Recommended.objects.create(
                user=request.user, 
                emotion=emotion, 
                weather=weather, 
                food=food,
                recommended_movies=recommended_movies,  # 추천된 영화들을 저장
                recommended_genres=genres,
            )

             # 저장된 인스턴스 직렬화
            today_serializer = TodaySerializer(recommended_instance)

            return Response({ 
                'recommended_genres': genres,
                'recommended_movies': movie_serializer.data,
                'today_serializer': today_serializer.data }
                , status=status.HTTP_200_OK)
