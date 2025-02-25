from django.db import models
from django.conf import settings

class Actor(models.Model):
    name = models.CharField(max_length=100, null=True)
    original_name = models.CharField(max_length=100, null=True)
    popularity = models.IntegerField(null=True)
    profile_path = models.CharField(max_length=20, null=True)
    like_users = models.ManyToManyField(
         settings.AUTH_USER_MODEL, related_name='like_actors'
    )

class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True, default=0)
    vote_average = models.FloatField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    poster_path = models.CharField(max_length=200)
    genres = models.CharField(max_length=20)
    backdrop_path= models.TextField(null=True, blank=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_movies'
    )
    actors = models.ManyToManyField(Actor, related_name='movies')


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_reviews")
    content = models.TextField()
    rating = models.PositiveSmallIntegerField()  # 1~5 사이의 점수
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return f"Review for {self.movie.title} by {self.user}"

class Recommended(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recommends")
    emotion = models.IntegerField(null=True)  # 사용자의 기분 (1~100 범위로 저장)
    weather = models.CharField(max_length=100)  # 날씨 
    food = models.CharField(max_length=100)  # 음식
    created_at = models.DateTimeField(auto_now_add=True)  # 저장 시간
    recommended_movies = models.TextField(blank=True, null=True)
    recommended_genres = models.TextField(blank=True, null=True)
