<template>
  <div class="container">
    <div class="gradient-header">
          <div 
            v-for="candy in candies" 
            :key="candy" 
            :class="['candy',candy.class]"
            style="cursor: pointer;"
            @click.prevent.stop="goToRandom"
          >
            <img :src="candy.image" class="candy-svg" :style="{ transform: `rotate(${candy.rotation}deg)` }">
          </div>

          <div class="header-text">
            <h1 class="main-text">Sweet Movies</h1>
            <p class="sub-text">영화 한 편, 사탕처럼 달콤한 순간을 맛보세요!</p>
          </div>

          <div class="gradient-content">
          </div>
      </div>

   

      <h3 class="text-left mt-4">솜사탕처럼 부드럽고 따끈따끈한 영화들</h3>
      <!-- 최신 영화 Carousel -->
      <div id="latestMovieCarousel" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <!-- 영화들을 그룹으로 나누기 (한 슬라이드에 6개씩) -->
        <div 
          v-for="(group, index) in movieGroups1" 
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
      <button class="carousel-control-prev" type="button" data-bs-target="#latestMovieCarousel" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#latestMovieCarousel" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>

      <h3 class="text-left mt-4">과자처럼 자꾸 손이 가는, 인기 영화들</h3>
      <!-- 인기 영화 Carousel -->
      <div id="popularityMovieCarousel" class="carousel slide" data-bs-ride="carousel">
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
      <button class="carousel-control-prev" type="button" data-bs-target="#popularityMovieCarousel" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#popularityMovieCarousel" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>

    <h3 class="text-left mt-4">쫀득한 평점, 젤리처럼 기분 좋은 영화들</h3>
      <!-- 평점 영화 Carousel -->
      <div id="voteMovieCarousel" class="carousel slide" data-bs-ride="carousel">
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
      <button class="carousel-control-prev" type="button" data-bs-target="#voteMovieCarousel" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#voteMovieCarousel" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>


  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useMovieStore } from '@/stores/movie';
import logo from '@/assets/로고.svg'
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useMovieStore();

const latest = ref([])
const popularity = ref([])
const vote = ref([])
// 사탕 이미지 배열 만들기
const candyImages = Array.from({ length: 11 }, (_,i) => `src/assets/candy/candy${i+1}.svg`)

// 랜덤 사탕생성
const getRandomCandy = () => {
  const randomIndex = Math.floor(Math.random() * candyImages.length);
  return candyImages[randomIndex];
};

// 각 사탕 객체에 대한 초기 데이터
const candies = ref(Array.from({ length: 8 }, (_, index) => ({
  id: index + 1,
  image: getRandomCandy(),
  class: `candy${index + 1}`,
  rotation: Math.random() * 360
})));

const goToRandom = function () {
  console.log('goToRandom 함수 실행');
  router.push({ name: 'movierandom' })
}


// 주기적으로 사탕 이미지 변경
onMounted(() => {
  setInterval(() => {
    candies.value = candies.value.map(candy => ({
      ...candy,
      image: getRandomCandy(),
      rotation: Math.random() * 360
    }));
  }, 30000); // 8초마다 이미지 변경
});



const movieGroups1 = computed(() => {
  const itemsPerSlide = 6;
  const groups = [];
  for (let i = 0; i < latest.value.length; i += itemsPerSlide) {
    groups.push(latest.value.slice(i, i + itemsPerSlide));
  }
  return groups;
});

const movieGroups2 = computed(() => {
  const itemsPerSlide = 6;
  const groups = [];
  for (let i = 0; i < popularity.value.length; i += itemsPerSlide) {
    groups.push(popularity.value.slice(i, i + itemsPerSlide));
  }
  return groups;
});

const movieGroups3 = computed(() => {
  const itemsPerSlide = 6;
  const groups = [];
  for (let i = 0; i < vote.value.length; i += itemsPerSlide) {
    groups.push(vote.value.slice(i, i + itemsPerSlide));
  }
  return groups;
});


onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/latest/`,
  })
  .then(res => {
    console.log(res.data)
    latest.value = res.data
  })
  .catch(err => {
    console.log(err)
  })
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/popularity/`, // 두 번째 API URL
  })
    .then(res => {
      console.log(res.data)
      popularity.value = res.data
    })
    .catch(err => {
      console.error(err)
    })
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/vote/`, // 세 번째 API URL
  })
    .then(res => {
      console.log(res.data)
      vote.value = res.data
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






/* 상단이미지 */


.gradient-header {
  width: 100%;
  height: 400px;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
  border-radius: 20px;
  background: linear-gradient(
    45deg,
    rgba(168,237,234,1) 0%,
    rgba(254,214,227,1) 100%
  );
  background-size: 400% 400%;
  animation: gradientMove 15s ease infinite;
}

.candy {
  position: absolute;
  width: 40px;
  height: 40px;
  pointer-events: auto;
  z-index: 2;
  transition: transform 0.3s ease;
}

.candy:hover {
  transform: scale(1.2);
}

.candy-svg {
  width: 100%;
  height: 100%;
  transition: transform 0.5s ease;
}

/* 사탕 위치 및 애니메이션 다양화 */
.candy1 {
  top: 15%;
  left: -50px;
  animation: rollRight 8s linear infinite;
}

.candy2 {
  top: 45%;
  right: -50px;
  animation: rollLeft 7s linear infinite;
  animation-delay: 1s;
}

.candy3 {
  bottom: -50px;
  left: 30%;
  animation: rollUp 6s linear infinite;
  animation-delay: 2s;
}

.candy4 {
  top: -50px;
  left: 60%;
  animation: rollDown 9s linear infinite;
  animation-delay: 1.5s;
}

.candy5 {
  top: 60%;
  left: -50px;
  animation: rollDiagonal 7.5s linear infinite;
  animation-delay: 0.5s;
}

.candy6 {
  top: 25%;
  right: -50px;
  animation: rollLeft 6.5s linear infinite;
  animation-delay: 3s;
}

.candy7 {
  bottom: -50px;
  right: 40%;
  animation: rollDiagonalReverse 8.5s linear infinite;
  animation-delay: 2.5s;
}

.candy8 {
  top: -50px;
  right: 25%;
  animation: rollDown 7s linear infinite;
  animation-delay: 1.8s;
}

@keyframes rollRight {
  from {
    left: -50px;
    transform: rotate(0deg);
  }
  to {
    left: calc(100% + 50px);
    transform: rotate(360deg);
  }
}

@keyframes rollLeft {
  from {
    right: -50px;
    transform: rotate(0deg);
  }
  to {
    right: calc(100% + 50px);
    transform: rotate(-360deg);
  }
}

@keyframes rollUp {
  from {
    bottom: -50px;
    transform: rotate(0deg);
  }
  to {
    bottom: calc(100% + 50px);
    transform: rotate(360deg);
  }
}

@keyframes rollDown {
  from {
    top: -50px;
    transform: rotate(0deg);
  }
  to {
    top: calc(100% + 50px);
    transform: rotate(-360deg);
  }
}

@keyframes rollDiagonal {
  0% {
    left: -50px;
    top: 100%;
    transform: rotate(0deg);
  }
  100% {
    left: calc(100% + 50px);
    top: -50px;
    transform: rotate(720deg);
  }
}

@keyframes rollDiagonalReverse {
  0% {
    right: -50px;
    top: 100%;
    transform: rotate(0deg);
  }
  100% {
    right: calc(100% + 50px);
    top: -50px;
    transform: rotate(-720deg);
  }
}

@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.header-text {
  position: absolute;
  bottom: 40px;
  left: 40px;
  z-index: 2;
}

.main-text {
  font-size: 3.5rem;
  font-weight: 700;
  color: var(--header-text);
  margin: 0;
  line-height: 1.2;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.sub-text {
  font-size: 1.5rem;
  color: var(--header-text);
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}
</style>
