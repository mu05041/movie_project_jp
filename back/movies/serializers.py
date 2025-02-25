from rest_framework import serializers
from .models import Movie, Review, Actor, Recommended


# 배우 목록 조회
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

# 영화 목록 조회
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'release_date',
            'popularity',
            'vote_average',
            'poster_path',
            'genres',
            'backdrop_path',
        )

# 리뷰 목록 조회
class ReviewListSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'content', 'rating', 'created_at', 'user_username', 'user')
        read_only_fields = ('user', 'movie',)  # movie도 read_only로 설정

# 리뷰 상세 조회
class ReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)  # movie_id 추가
    
    class Meta:
        model = Review
        # 'user_username'와 'movie_title'을 명시적으로 추가합니다.
        fields = ('id', 'content', 'rating', 'movie_title', 'user','user_username', 'movie_id', )
        read_only_fields = ('user','movie',)

# 영화 상세 조회
class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    reviews = ReviewListSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'release_date',
            'popularity',
            'vote_average',
            'overview',
            'poster_path',
            'genres',
            'reviews',
            'backdrop_path',
            'actors',
        )

    def get_genres(self, obj):
        # 문자열을 리스트로 변환
        if isinstance(obj.genres, str):
            import json
            try:
                return json.loads(obj.genres.replace("'", '"'))
            except json.JSONDecodeError:
                # 실패하면 기본 파싱 시도
                genres_str = obj.genres.strip('[]').replace("'", "")
                return [g.strip() for g in genres_str.split(',') if g.strip()]
            # genres가 이미 리스트라면 그대로 반환
        elif isinstance(obj.genres, list):
            return obj.genres
        return []

# 영화 검색
class MovieSearchSerializer(serializers.ModelSerializer):
    similarity = serializers.FloatField(default=0)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path', 'similarity',)

# mainlogic 
class TodaySerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Recommended
        fields = ('emotion', 'food', 'weather', 'user_username', 'recommended_genres',)
        read_only_fields = ('user', 'recommended_genres')