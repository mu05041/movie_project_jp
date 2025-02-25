<template>
  <div class="container">
    <!-- 아이디어로직 -->
      <!-- TodayMovie 섹션 -->
      <div>
        <TodayMovie />
      </div>


    <h2 class="text-left mt-4" v-if="movieGroups.length">좋아요 기반 영화추천</h2>
    
    <!-- 첫 번째 Carousel (좋아요 기반 추천) -->
    <div id="movieCarousel" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <!-- 영화들을 그룹으로 나누기 (한 슬라이드에 6개씩) -->
        <div 
          v-for="(group, index) in movieGroups" 
          :key="index"
          class="carousel-item"
          :class="{ active: index === 0 }"
        >
          <div class="movie-row">
            <div 
              v-for="movie in group" 
              :key="movie.id"
              class="movie-card-wrapper"
            >
              <RouterLink 
                :to="{ name: 'moviedetail', params: { movieId: movie.id } }"
                class="movie-card-link"
              >
                <div class="movie-card">
                  <img 
                    :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" 
                    :alt="movie.title" 
                    class="card-img"
                  >
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 컨트롤 버튼 -->
       <span v-if="movieGroups.length">
        <button class="carousel-control-prev" type="button" data-bs-target="#movieCarousel" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#movieCarousel" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
    </span>
    </div>

    <h2 class="text-left mt-4">{{ season }}에는 이런 영화 어떠세요?</h2>
    
    <!-- 두 번째 Carousel (계절 기반 추천) -->
    <div id="seasonMovieCarousel" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <!-- 영화들을 그룹으로 나누기 (한 슬라이드에 6개씩) -->
        <div 
          v-for="(group, index) in movieGroups2" 
          :key="index"
          class="carousel-item"
          :class="{ active: index === 0 }"
        >
          <div class="movie-row">
            <div 
              v-for="movie in group" 
              :key="movie.id"
              class="movie-card-wrapper"
            >
              <RouterLink 
                :to="{ name: 'moviedetail', params: { movieId: movie.id } }"
                class="movie-card-link"
              >
                <div class="movie-card">
                  <img 
                    :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" 
                    :alt="movie.title" 
                    class="card-img"
                  >
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 컨트롤 버튼 -->
      <button class="carousel-control-prev" type="button" data-bs-target="#seasonMovieCarousel" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#seasonMovieCarousel" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>

    <h2 class="text-left mt-4" v-if="movieGroups3.length">당신이 좋아하는 배우의 숨겨진 명작을 발견해보세요!</h2>

    <!-- 세 번째 Carousel (배우 좋아요 기반 추천) -->
    <div id="seasonMovieCarousel" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <!-- 영화들을 그룹으로 나누기 (한 슬라이드에 6개씩) -->
        <div 
          v-for="(group, index) in movieGroups3" 
          :key="index"
          class="carousel-item"
          :class="{ active: index === 0 }"
        >
          <div class="movie-row">
            <div 
              v-for="movie in group" 
              :key="movie.id"
              class="movie-card-wrapper"
            >
              <RouterLink 
                :to="{ name: 'moviedetail', params: { movieId: movie.id } }"
                class="movie-card-link"
              >
                <div class="movie-card">
                  <img 
                    :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" 
                    :alt="movie.title" 
                    class="card-img"
                  >
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 컨트롤 버튼 -->
      <button class="carousel-control-prev" type="button" data-bs-target="#actorMovieCarousel" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#actorMovieCarousel" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useMovieStore } from '@/stores/movie'
import { useRouter, useRoute } from 'vue-router'
import TodayMovie from '@/views/TodayMovie.vue'
import mainimage from '@/assets/메인이미지.png'



const store = useMovieStore()
const router = useRouter()
const recommendmovies = ref([]) // 좋아요 기반 추천
const recommendmovies2 = ref([]) // 계절 기반 추천
const recommendmovies3 = ref([]) // 좋아하는 배우의 다른 영화 추천

const season = ref(null)


// 첫 번째 카로셀의 영화 배열을 그룹으로 나누는 computed 속성
const movieGroups = computed(() => {
  const itemsPerSlide = 6 // 한 슬라이드당 보여줄 영화 수
  const groups = []
  
  for (let i = 0; i < recommendmovies.value.length; i += itemsPerSlide) {
    groups.push(recommendmovies.value.slice(i, i + itemsPerSlide))
  }
  
  return groups
})

// 두 번째 카로셀의 영화 배열을 그룹으로 나누는 computed 속성
const movieGroups2 = computed(() => {
  const itemsPerSlide = 6
  const groups = []
  
  for (let i = 0; i < recommendmovies2.value.length; i += itemsPerSlide) {
    groups.push(recommendmovies2.value.slice(i, i + itemsPerSlide))
  }
  
  return groups
})

// 세 번째 카로셀의 영화 배열을 그룹으로 나누는 computed 속성
const movieGroups3 = computed(() => {
  const itemsPerSlide = 6
  const groups = []
  
  for (let i = 0; i < recommendmovies3.value.length; i += itemsPerSlide) {
    groups.push(recommendmovies3.value.slice(i, i + itemsPerSlide))
  }
  
  return groups
})



onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/recommend/like/`, // 첫 번째 API URL
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(res => {
      recommendmovies.value = res.data
      console.log(res.data)
    })
    .catch(err => {
      console.error(err)
    })
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/recommend/season/`, // 두 번째 API URL
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(res => {
      season.value = res.data.season
      recommendmovies2.value = res.data.recommended_movies
      console.log(res.data.season)
      console.log(res.data.recommended_movies)
    })
    .catch(err => {
      console.error(err)
    })
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/recommend/actor/`, // 세 번째 API URL
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(res => {
      console.log(res.data)
      recommendmovies3.value = res.data
    })
    .catch(err => {
      console.error(err)
    })
})



</script>

<style scoped>
.container {
  padding: 0.75rem;
}

.carousel {
  position: relative;
  padding: 0 50px; /* 좌우 버튼을 위한 여백 */
}

.movie-row {
  display: flex;
  gap: 20px;
  padding: 20px 0;
}

.movie-card-wrapper {
  flex: 0 0 calc(16.666% - 17px); /* 6개의 카드를 균등하게 배치 */
  max-width: calc(16.666% - 17px);
}

.movie-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.movie-card {
  background-color: white;
  border-radius: 15px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-img {
  width: 100%;
  height: auto;
  aspect-ratio: 2/3;
  object-fit: cover;
  display: block;
  border-radius: 15px;
}

.movie-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

/* Carousel 컨트롤 스타일 수정 */
.carousel-control-prev,
.carousel-control-next {
  width: 40px;
  background-color: rgba(0,0,0,0.3);
  border-radius: 50%;
  height: 40px;
  top: 50%;
  transform: translateY(-50%);
}

.carousel-control-prev {
  left: 0;
}

.carousel-control-next {
  right: 0;
}

/* 메인 이미지 스타일 */
.main-image-wrapper {
  height: 100%;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 15px;
}




/* 반응형 디자인 */
@media (max-width: 1200px) {
  .movie-card-wrapper {
    flex: 0 0 calc(20% - 16px); /* 5개 카드 */
    max-width: calc(20% - 16px);
  }
}

@media (max-width: 992px) {
  .movie-card-wrapper {
    flex: 0 0 calc(25% - 15px); /* 4개 카드 */
    max-width: calc(25% - 15px);
  }
}

@media (max-width: 768px) {
  .movie-card-wrapper {
    flex: 0 0 calc(33.333% - 14px); /* 3개 카드 */
    max-width: calc(33.333% - 14px);
  }
}

@media (max-width: 576px) {
  .movie-card-wrapper {
    flex: 0 0 calc(50% - 10px); /* 2개 카드 */
    max-width: calc(50% - 10px);
  }
}
</style>
