<template>
  <div class="container">
    <div class="header-wrapper">
  <div class="candy">
    <RollingCandy />
  </div>
  <h2 class="title my-4">CineBite, 영화의 다양한 맛을 경험하세요!</h2>
</div>
  
  <!-- <h1 class="text-center my-4">시네바이트, 영화의 다양한 맛을 경험하세요!</h1> -->
    <!-- 정렬 기준 선택 -->
    <div class="sort-options mb-4 text-center">
      <div class="btn-group" role="group" aria-label="정렬 기준">
        <button 
          type="button" 
          class="btn gradient-btn" 
          :class="{ active: orderBy === 'latest' }"
          @click="selectOrder('latest')"
        >
          최신순
        </button>
        <button 
          type="button" 
          class="btn gradient-btn" 
          :class="{ active: orderBy === 'vote_average' }"
          @click="selectOrder('vote_average')"
        >
          평점순
        </button>
        <button 
          type="button" 
          class="btn gradient-btn" 
          :class="{ active: orderBy === 'popularity' }"
          @click="selectOrder('popularity')"
        >
          인기순
        </button>
      </div>
    </div>

    <!-- 첫 번째 Carousel -->
    <div id="movieCarousel" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <!-- 영화들을 그룹으로 나누기 -->
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



    <div class="row gy-4">
      <div
        class="col-12 col-sm-6 col-md-4 col-lg-3"
        v-for="movie in store.movies"
        :key="movie.id"
      >
        <div class="custom-movie-container">
          <RouterLink
            :to="{ name: 'moviedetail', params: { movieId: movie.id } }"
            class="image-link"
          >
            <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" 
                 alt="Movie Poster" 
                 class="movie-poster">
          </RouterLink>
          <h3 class="movie-title px-3 pt-2">{{ movie.title }}</h3>
          <div class="movie-footer">
            <div class="rating-container">
              <span class="star-icon filled">★</span>
              <span class="vote-average ms-2">{{ movie.vote_average.toFixed(1) }}</span>
            </div>
            <button
              @click="toggleLike(movie)"
              class="btn btn-sm btn-like"
            >
              <span
                class="like-icon"
                :class="movie.isLiked ? 'text-danger' : 'text-secondary'"
              >
                {{ movie.isLiked ? '❤️' : '🤍' }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { RouterLink } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import { onMounted, computed, ref } from 'vue'
import axios from 'axios'
import RollingCandy from './RollingCandy.vue';

const store = useMovieStore()

// 상태 변수 관리
const movies = ref([]); // 선택 영화
const orderBy = ref('latest'); // 기본 정렬 기준

const movieGroups = computed(() => {
  const itemsPerSlide = 6;
  const groups = [];
  for (let i = 0; i < movies.value.length; i += itemsPerSlide) {
    groups.push(movies.value.slice(i, i + itemsPerSlide));
  }
  return groups;
});

// 영화 데이터를 가져오는 메서드
const fetchMovies = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/sorted/`,
    params: {
      order_by: orderBy.value,
    },
  })
    .then((res) => {
      movies.value = res.data;
    })
    .catch((err) => {
      console.error('Error fetching movies:', err);
    });
};

// 정렬 기준 선택 메서드
const selectOrder = (order) => {
  orderBy.value = order;
  fetchMovies();
};

onMounted(() => {
  store.getMovieLists()
  fetchMovies();

})

const toggleLike = function (movie) {
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/movies/${movie.id}/like/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(res => {
      console.log(res.data)
      movie.isLiked = res.data.is_liked
      movie.likeCount = res.data.like_count
      store.updateLocalStorage(movie)
    })
    .catch(err => {
      console.log('좋아요 상태 변경 실패:', err)
    })
}

const likedMovies = computed(() => store.movies.filter((movie) => movie.isLiked))
</script>

<style scoped>
.gradient-btn {
  background:  #FFB6C1; /* 연한 핑크색과 녹색 그라데이션 */
  border:none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  padding: 0.5rem 1rem;
  font-weight: bold;
  transition: all 0.3s ease;
}

.gradient-btn:hover {
  background: linear-gradient(45deg, #92ebcd, #FFB3C1); /* 호버 시 더 연한 녹색과 핑크색 조합 */
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.gradient-btn:focus {
  background: #92ebcd;
  outline: none;
  box-shadow: 0 0 10px rgba(255, 182, 193, 0.6); /* 연한 핑크색 빛나는 효과 */
}


.custom-movie-container {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease;
}

.custom-movie-container:hover {
  transform: translateY(-5px);
}

.movie-poster {
  width: 100%;
  aspect-ratio: 2/3;
  object-fit: cover;
}

.movie-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.movie-footer {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.rating-container {
  display: flex;
  align-items: center;
}

.star-icon {
  font-size: 1.2rem;
  color: #6c757d;
}

.star-icon.filled {
  color: #f39c12;
}

.btn-like {
  background: rgba(255, 255, 255, 0.15);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.btn-like:hover {
  background: rgba(255, 255, 255, 0.25);
}

a {
  text-decoration: none;
  color: inherit;
}


.carousel {
  position: relative;
  padding: 0 50px; /* 좌우 버튼을 위한 여백 */
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

.header-wrapper {
  text-align: center;
  padding-top: 2rem; /* 상단 여백 */
}

.candy {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem; /* 텍스트와의 간격 */
}

.title {
  text-align: center;
  margin: 0;
}
</style>