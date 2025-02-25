from rest_framework import serializers
from .models import User
from movies.models import Review, Movie, Actor
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','followers','followings',)


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)
        
class ReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'content', 'movie_title', 'created_at', 'rating', 'movie_id']

# 프로필에 보내주는 영화 정보(좋아요한 영화 보여주기)
class ProfileMovieSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()  # 좋아요 상태를 추가할 필드

    class Meta:
        model = Movie
        fields = '__all__'  # 모든 필드 포함
    
    def get_is_liked(self, obj):
        # 현재 요청을 보낸 사용자가 해당 영화를 좋아요했는지 확인
        user = self.context.get('request').user
        return user in obj.like_users.all()  # 사용자가 좋아요한 영화인지 확인


# 프로필에 보내주는 배우 정보(좋아요한 배우 보여주기)
class ProfileActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields ='__all__'
