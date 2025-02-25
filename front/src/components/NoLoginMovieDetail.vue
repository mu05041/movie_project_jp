<template>
    <div class="container px-3">
      <div class="movie-container">
        <div class="movie-poster">
          <img :src="posterUrl" alt="Movie Poster" class="movie-image">
        </div>
        <div class="movie-details">
          <h1>{{ movieDetails.title }}</h1>
          <p>개봉일 : {{ movieDetails.release_date }}</p>
          <h4>장르</h4>
          <div v-for="genre in movieDetails.genres" :key="genre.id" class="inline-genre">
            <p>{{ genre }} |</p>
          </div>
          <h4>줄거리</h4>
          <p>{{ movieDetails.overview }}</p>
        </div>
      </div>
      <hr>
      <div class="actor-information mt-4">
        <div class="row justify-content-start">
          <div
            v-for="actor in movieDetails.actors" 
            :key="actor.id"
            class="col-4 col-sm-3 col-md-2 mb-4 actor-card"
            style="cursor: pointer;"
          >
            <div class="text-center">
              <div class="img-container">
                <img 
                  :src="`https://image.tmdb.org/t/p/w500${actor.profile_path}`"
                  alt="profile"
                  class="actor-image">
              </div>
              <p class="actor-name">{{ actor.name }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  
  const props = defineProps({
    movieDetails: Object
  });
  
  const posterUrl = computed(() => `https://image.tmdb.org/t/p/w500${props.movieDetails.poster_path}`);
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400&display=swap');
  
  .container {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
    font-family: "IBM Plex Sans KR", sans-serif;
    font-weight: 400;
    font-style: normal;
  }
  
  .movie-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    margin-top: 20px;
    gap: 20px;
  }
  
  .movie-poster {
    flex: 1;
    text-align: center;
  }
  
  .movie-image {
    width: 250px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .movie-details {
    flex: 2;
    text-align: left;
  }
  
  .inline-genre {
    display: inline-block;
    margin-right: 5px;
    color: #6c757d;
  }
  
  .actor-card {
    padding: 10px;
  }
  
  .img-container {
    width: 100px;
    height: 100px;
    margin: 0 auto;
    border-radius: 50%;
    overflow: hidden;
  }
  
  .actor-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.2s;
  }
  
  .actor-image:hover {
    transform: scale(1.05);
  }
  
  .actor-name {
    margin-top: 8px;
    font-size: 0.9rem;
    color: #333;
    text-align: center;
    word-break: keep-all;
    line-height: 1.2;
  }
  </style>
  