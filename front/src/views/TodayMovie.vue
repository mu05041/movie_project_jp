<template>
  <div class="container">
    <div class="row">
      <!-- TodayMovie 섹션 -->
      <div class="col-12 col-lg-6">
        <div class="today-movie-section">
          <h2>오늘의 영화추천</h2>
          
          <!-- 기분 슬라이더 -->
          <div class="mt-4">
            <div class="slider-container">
              <input 
                type="range" 
                v-model="emotion" 
                min="0" 
                max="100" 
                class="slider"
                id="myrange"
              >
              <div class="row mt-2 text-center">
                <div class="col-4"><span>차분함</span></div>
                <div class="col-4"><span>보통</span></div>
                <div class="col-4"><span>신남</span></div>
              </div>
              
              <!-- 날씨 선택 -->
              <div class="button-section mt-4">
                <button 
                  class="btn btn-outline-info me-2 mb-2"
                  v-for="weather in weathers"
                  :key="weather"
                  @click="selectedWeather(weather)"
                  :class="{ selected: selectWeather === weather.text }"
                >
                  <img :src="weather.icon" class="icon-small" /> {{ weather.text }}
                </button>
              </div>
              
              <!-- 음식선택 -->
              <div class="button-section mt-4">
                <button
                  class="btn btn-outline-info me-2 mb-2"
                  v-for="food in foods"
                  :key="food"
                  @click="selectedFood(food)"
                  :class="{ selected: selectfood === food.text }"
                >
                  <img :src="food.icon" class="icon-small" /> {{ food.text }}
                </button>
              </div>
              <!-- <div class="mt-2">선택된 값: {{ emotion }}</div> -->
              
              <!-- 추천 버튼 -->
              <div class="button-section mt-4">
                <button
                  @click="getRecommendation"
                  class="btn btn-outline-success"
                >
                  {{ isLoading ? '검색중...' : '추천 받기' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 메인 이미지 섹션 -->
    
      <div class="col-12 col-lg-6">
        <div class="main-image-wrapper">
          <span id="addcomment">
          <img 
          v-if="mainimage" 
            :src="mainimage" 
            alt="Featured Movie" 
            class="main-image"
          />
        </span>
        </div>
      </div>

      
    </div>

    <!-- 추천 결과 섹션 -->
    <div class="result mt-4">
      <div v-if="mymovie">
        <h3 v-if="emotion !== null && selectWeather !== '' && selectfood !== '' && recommended_genres.length > 0">
          {{ username }}에게 어울리는 영화 장르는 
          {{ recommended_genres.join(', ') }}입니다.
        </h3>
        <div class="row g-4">
          <div v-for="movie in mymovie"
               :key="movie.id"
               class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2">
            <RouterLink 
              :to="{ name: 'moviedetail', params: { movieId: movie.id } }"
              class="movie-card-link"
            >
              <div class="movie-card bounce-in-right">
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
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useMovieStore } from '@/stores/movie'

// 아이콘 이미지 가져오기
import 젤리Icon from '@/assets/icons/젤리.png'
import 초콜릿Icon from '@/assets/icons/초콜릿.png'
import 사탕Icon from '@/assets/icons/사탕.png'
import 과자Icon from '@/assets/icons/과자.png'
import 맑음Icon from '@/assets/icons/맑음.png'
import 흐림Icon from '@/assets/icons/흐림.png'
import 비Icon from '@/assets/icons/비.png'
import 눈Icon from '@/assets/icons/눈.png'
import mainimage from '@/assets/메인이미지.png'
import 사탕일러스트 from '@/assets/사탕일러스트.svg'
import 초콜릿일러스트 from '@/assets/초콜릿일러스트.svg'
import 젤리일러스트 from '@/assets/젤리일러스트.svg'
import 과자일러스트 from '@/assets/과자일러스트.svg'


// 상태 관리
const store = useMovieStore()
const emotion = ref(20)
const weathers = ref([
  { text: '맑음', icon: 맑음Icon },
   { text: '흐림', icon: 흐림Icon },
   { text: '비', icon: 비Icon },
   { text: '눈', icon: 눈Icon },
])
const foods = ref([
  { text: '젤리', icon: 젤리Icon },
  { text: '초콜릿', icon: 초콜릿Icon },
  { text: '사탕', icon: 사탕Icon },
  { text: '과자', icon: 과자Icon }
])



let selectWeather = ref('')
let selectfood = ref('')
const isLoading = ref(false)


const selectedWeather = (res) => {
    console.log(res)
    selectWeather.value = res.text
  
}

const selectedFood = (res) => {
    console.log(res)
    selectfood.value = res.text

}

const mymovie = ref([])
const recommended_genres = ref([])
const username = ref(null)

const getRecommendation = function () {
axios({
  method: 'post',
  url: `${store.API_URL}/api/v1/movies/recommend/today/`,
  headers: {
    Authorization: `Token ${store.token}`
  },
  data: {
    emotion: emotion.value,
    weather: selectWeather.value,
    food: selectfood.value,
  }
})
  .then(res => {
    console.log(res.data)
    console.log(res.data.recommended_movies)
    console.log(res.data.recommended_genres)
    mymovie.value = res.data.recommended_movies
    recommended_genres.value = res.data.recommended_genres
    username.value = res.data.today_serializer.user_username
    getComment({food:selectfood.value})

  })
  .catch(err => {
    console.log(err)
  })
}


const getComment = function (data) {
  const commentWraper = document.getElementById('addcomment')
  // maininamge를 텍스트로 바꿔쳐야함
  const comments = {
    '초콜릿': '녹아내리는 초콜릿처럼 진한 로맨스와 멜로 속으로 빠져보세요. 한 입 베어 물 때마다 사랑의 감정이 퍼져나가는 그 달콤한 순간을 만끽하세요!',
    '사탕': '녹을수록 강렬해지는 사탕처럼, 모험과 판타지의 짜릿한 세계로 당신을 초대합니다!',
    '젤리': '쫄깃하게 즐기는 드라마와 액션! 감정이 휘몰아치는 이야기와 박진감 넘치는 액션 영화로, 달콤하고 상큼한 순간을 만끽해보세요!',
    '과자':'가볍고 바삭한 과자처럼, 부담 없이 애니메이션과 가족 영화로 함께 편안한 시간을 즐기고, 다큐멘터리와 역사의 세계까지 바삭하게 탐험해보세요!',
  }
  const illustrations = {
    '초콜릿': 초콜릿일러스트,
    '사탕': 사탕일러스트,
    '젤리': 젤리일러스트,
    '과자': 과자일러스트
  }

    console.log('초콜릿 조건 만족')
    commentWraper.innerHTML = `
       <h5 style="padding: 20px">${comments[data.food]}</h5>
           <img 
            src="${illustrations[data.food]}" 
            alt="${data.food} 일러스트" 
            class="jello-horizontal"
            style="width: 100%; height: 300px; object-fit: contain; padding: 20px;
            padding-bottom: 40px;"
            >



    `

  }


</script>



<style scoped>
/* .entire-container{
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;

} */

.btn-outline-info {
  /* width:120px; */
  /* width:20%; */
  --bs-btn-padding-y: 0.25rem;
  --bs-btn-padding-x: 1rem; 
  --bs-btn-font-size: 1.3rem;
  --bs-btn-color: #ac2eb8
  padding: var(--bs-btn-padding-y) var(--bs-btn-padding-x);

  white-space: nowrap; /* 줄바꿈 방지 */
  display: inline-flex; /* 아이콘과 텍스트를 한 줄로 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  justify-content: center; /* 가로 중앙 정렬 */


  /* 호버(마우스 오버) 상태 */
  --bs-btn-hover-color: #F19ED2;                  /* 호버시 텍스트 색상 */
  --bs-btn-hover-bg: #a8edea;                
  --bs-btn-hover-border-color: #a8edea;  
  /* 활성화(클릭) 상태 */
  --bs-btn-active-color: #fed6e3;                  
  --bs-btn-active-bg: #fed6e3;       
  --bs-btn-active-border-color: #fed6e3;     /* 활성화시 테두리 색상 */
}
.btn-outline-success {
  width:100%;
  --bs-btn-padding-y: 0.25rem;
  --bs-btn-padding-x: 1rem; 
  --bs-btn-font-size: 1.7rem;
  padding: var(--bs-btn-padding-y) var(--bs-btn-padding-x);
  font-size: var(--bs-btn-font-size);

}

/* 날씨 & 음식 버튼  */
.button-section {
  display: flex;
  gap: 5px;
  width: 100%;
}

.button-section button {
  flex: 1;
  height: 45px;
}


/* 게이지 바 */
input[type=range] {
    -webkit-appearance: none; 
    overflow: hidden;
    width: 100%; 
    height: 20px;
    background: transparent; 
    cursor: pointer;
    background: #ffbed1;
    /* background: linear-gradient(90deg, #ffe0e9, rgb(255, 169, 186)); */
  
    border-radius: 20px;
  }

  input[type=range]:focus {
    outline: none; 
  }
/* 게이지 버튼 */
  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 10px;
    height: 20px;
    background: #ffffff;
    box-shadow: -100vw 0 0 100vw #a8edea	;
    border: 0.1px solid #ffffff	;
    cursor: pointer;
    border-radius: px;

  }

  /* 영화 추천하기 버튼 */
  .btn-outline-success {
    background: linear-gradient(45deg, #90f3d2, #FFB6C1);
    border: none;
    color: white;
    transition: all 0.3s ease;
  }

  .btn-outline-success:hover {
    background: linear-gradient(45deg, #7FFFD4, #FF69B4);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  }


  /* 메인이미지 */
  .today-movie-section {
  padding: 1rem;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 100%;

}

.main-image-wrapper {
  height: 100%;
  height: 400px;
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


  /* 영화 추천 보여주기 */

.container {
  padding: 0.75rem;
}

.movie-card {
  background-color: white;
  border-radius: 15px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.movie-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
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



.movie-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.result {
  padding: 0.75rem;
}

.movie-grid {
  display: flex;
  flex-wrap: wrap;
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

.result h3 {
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
  font-weight: 600;
}


/* 아이콘 사이즈 변경하기 */
.icon-small {
  width: 20px;
  height: 20px;
  vertical-align: middle;
  margin-right: 4px;
}
.selected {
  background-color: #a8edea !important; /* 민트색 */
  border-color: #a8edea !important;
  color: white !important;
}




</style>

<!-- 전역 스타일 -->
<style>

.jello-horizontal {
	-webkit-animation: jello-horizontal 0.9s both;
	        animation: jello-horizontal 0.9s both;
}
 @-webkit-keyframes jello-horizontal {
  0% {
    -webkit-transform: scale3d(1, 1, 1);
            transform: scale3d(1, 1, 1);
  }
  30% {
    -webkit-transform: scale3d(1.25, 0.75, 1);
            transform: scale3d(1.25, 0.75, 1);
  }
  40% {
    -webkit-transform: scale3d(0.75, 1.25, 1);
            transform: scale3d(0.75, 1.25, 1);
  }
  50% {
    -webkit-transform: scale3d(1.15, 0.85, 1);
            transform: scale3d(1.15, 0.85, 1);
  }
  65% {
    -webkit-transform: scale3d(0.95, 1.05, 1);
            transform: scale3d(0.95, 1.05, 1);
  }
  75% {
    -webkit-transform: scale3d(1.05, 0.95, 1);
            transform: scale3d(1.05, 0.95, 1);
  }
  100% {
    -webkit-transform: scale3d(1, 1, 1);
            transform: scale3d(1, 1, 1);
  }
}
@keyframes jello-horizontal {
  0% {
    -webkit-transform: scale3d(1, 1, 1);
            transform: scale3d(1, 1, 1);
  }
  30% {
    -webkit-transform: scale3d(1.25, 0.75, 1);
            transform: scale3d(1.25, 0.75, 1);
  }
  40% {
    -webkit-transform: scale3d(0.75, 1.25, 1);
            transform: scale3d(0.75, 1.25, 1);
  }
  50% {
    -webkit-transform: scale3d(1.15, 0.85, 1);
            transform: scale3d(1.15, 0.85, 1);
  }
  65% {
    -webkit-transform: scale3d(0.95, 1.05, 1);
            transform: scale3d(0.95, 1.05, 1);
  }
  75% {
    -webkit-transform: scale3d(1.05, 0.95, 1);
            transform: scale3d(1.05, 0.95, 1);
  }
  100% {
    -webkit-transform: scale3d(1, 1, 1);
            transform: scale3d(1, 1, 1);
  }
}


/* 추천영화 등장 애니매에션 */
.bounce-in-right {
	-webkit-animation: bounce-in-right 1.1s both;
	        animation: bounce-in-right 1.1s both;
}

 @-webkit-keyframes bounce-in-right {
  0% {
    -webkit-transform: translateX(600px);
            transform: translateX(600px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
    opacity: 0;
  }
  38% {
    -webkit-transform: translateX(0);
            transform: translateX(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
    opacity: 1;
  }
  55% {
    -webkit-transform: translateX(68px);
            transform: translateX(68px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
  }
  72% {
    -webkit-transform: translateX(0);
            transform: translateX(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
  }
  81% {
    -webkit-transform: translateX(32px);
            transform: translateX(32px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
  }
  90% {
    -webkit-transform: translateX(0);
            transform: translateX(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
  }
  95% {
    -webkit-transform: translateX(8px);
            transform: translateX(8px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
  }
  100% {
    -webkit-transform: translateX(0);
            transform: translateX(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
  }
}

@keyframes bounce-in-right {
  0% {
    -webkit-transform: translateX(600px);
            transform: translateX(600px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
    opacity: 0;
  }
  38% {
    -webkit-transform: translateX(0);
            transform: translateX(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
    opacity: 1;
  }
  55% {
    -webkit-transform: translateX(68px);
            transform: translateX(68px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
  }
  72% {
    -webkit-transform: translateX(0);
            transform: translateX(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
  }
  81% {
    -webkit-transform: translateX(32px);
            transform: translateX(32px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
  }
  90% {
    -webkit-transform: translateX(0);
            transform: translateX(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
  }
  95% {
    -webkit-transform: translateX(8px);
            transform: translateX(8px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
  }
  100% {
    -webkit-transform: translateX(0);
            transform: translateX(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
  }
}


</style>