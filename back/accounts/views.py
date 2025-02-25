from rest_framework.response import Response
from rest_framework.decorators import api_view

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from movies.models import Movie, Review
from .serializers import ReviewSerializer, ProfileMovieSerializer, ProfileActorSerializer
from movies.serializers import MovieListSerializer
import requests


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    
    if person != request.user:
        if person.followers.filter(pk=request.user.pk).exists():
            person.followers.remove(request.user)
            is_followed = False
        else:
            person.followers.add(request.user)
            is_followed = True
            
        serializer = UserSerializer(person)
        return Response({
            'is_followed': is_followed,
            'followers_count': len(serializer.data['followers']),
            'followings_count': len(serializer.data['followings']),
            'user': serializer.data
        })
        
    return Response({
        'status': 'error',
        'message': '자신을 팔로우할 수 없습니다.'
    })

User = get_user_model()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    data = {
        'username': user.username,
        'is_followed': user.followers.filter(pk=request.user.pk).exists(),
        'followers_count': user.followers.count(),
        'followings_count': user.followings.count(),
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reviews(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    reviews = user.user_reviews.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

# 좋아요한 영화 보내주기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_liked_movies(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    liked_movies = user.like_movies.all()
    serializer = ProfileMovieSerializer(liked_movies, many=True, context={'request': request})
    return Response(serializer.data)

# 좋아요한 배우 보내주기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_liked_actors(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    liked_actors = user.like_actors.all()
    serializer = ProfileActorSerializer(liked_actors, many=True)
    return Response(serializer.data)