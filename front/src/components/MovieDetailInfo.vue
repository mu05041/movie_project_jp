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

        <div class="button-container">
        <button 
          class="btn mt-3"
          @click="openReviewModal"
        >
          리뷰 작성하기
        </button>

        <!-- 영화 좋아요 아이콘 추가 -->
        <button
          @click="toggleMovieLike(movieDetails)"
          class="btn btn-sm btn-like"
        >
          <span
            class="like-icon"
            :class="movieDetails.isLiked ? 'text-danger' : 'text-secondary'"
          >
          {{ movieDetails.isLiked ? '❤️' : '🤍' }}
          </span>
        </button>
        </div>
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
            <button
              @click="toggleActorLike(actor)"
              class="btn btn-sm btn-like"
            >
              <span
                class="like-icon"
                :class="actor.isLiked ? 'text-danger' : 'text-secondary'"
              >
                {{ actor.isLiked ? '❤️' : '🤍' }}
              </span>
            </button>

          </div>
        </div>
      </div>
    </div>
    
    <div v-if="movieDetails.reviews && movieDetails.reviews.length > 0">
      <ReviewListView />
    </div>

    <!-- 리뷰 작성 모달 -->
    <div v-show="isReviewModalOpen" class="modal" @click="closeReviewModalOnClickOutside">
      <div class="modal-content">
        <form @submit.prevent="submitReview">
          <!-- ReviewForm에 closeReviewModal 전달 -->
          <ReviewForm 
            :movieId="movieDetails.id" 
            :closeReviewModal="closeReviewModal" 
            :onReviewSubmitted="onReviewSubmitted" 
          />
        </form>
      </div>
    </div>

  </div>
</template>
<script setup>
import { computed, onMounted, ref } from 'vue';
import ReviewListView from '@/views/ReviewListView.vue'
import ReviewForm from './ReviewForm.vue';
import axios from 'axios';
import { useRouter,onBeforeRouteUpdate } from 'vue-router';
import { useMovieStore } from '@/stores/movie'

const store = useMovieStore()

const props = defineProps({
  movieDetails: {
    type: Object,
    required: true
  }
});

const router = useRouter();
const posterUrl = computed(() => `https://image.tmdb.org/t/p/w500${props.movieDetails.poster_path}`);

// 리뷰 작성 모달 상태
const isReviewModalOpen = ref(false);

// 리뷰 모달 열기/닫기 메서드
const openReviewModal = () => {
  isReviewModalOpen.value = true;
  console.log('리뷰 모달이 열렸습니다.')
};

const closeReviewModal = () => {
  isReviewModalOpen.value = false;
  router.push({ name: 'moviedetail' })

};

// 모달 외부 클릭 시 닫기
const closeReviewModalOnClickOutside = (event) => {
  if (event.target.classList.contains('modal')) {
    closeReviewModal();
  }
};

// 리뷰 제출 후 페이지 새로고침 및 moviedetail로 이동
const onReviewSubmitted = () => {
  window.location.reload()
  router.push({ name: 'moviedetail', params: { movieId: movie.id } })
}

const toggleMovieLike = (movie) => {
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/movies/${movie.id}/like/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(res => {
      movie.isLiked = res.data.is_liked
      updateLocalStorage(movie.id, res.data.is_liked)
      // 영화 데이터 다시 불러오기
      getMovieDetail()
    })
}
// 배우 토글
const toggleActorLike = (actor) => {
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/actors/${actor.id}/like/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(res => {
      // 서버 응답 데이터로 모든 상태 동기화
      console.log('actir data=',res.data)
      actor.isLiked = res.data.is_liked
      actor.likeCount = res.data.like_count
      // 로컬 스토리지 업데이트
      updateActorLocalStorage(actor.id, res.data.is_liked)
      
    })
    .catch(err => {
      console.error('Failed to update actortoggle', err)
    })
}

const updateActorLocalStorage = (actorId, isLiked) => {
  try {
    const likedActors = JSON.parse(localStorage.getItem('likedActors')) || []
    
    if (isLiked) {
      if (!likedActors.includes(actorId)) {
        likedActors.push(actorId)
      }
    } else {
      const index = likedActors.indexOf(actorId)
      if (index > -1) {
        likedActors.splice(index, 1)
      }
    }
    
    localStorage.setItem('likedActors', JSON.stringify(likedActors))
  } catch (err) {
    console.error('Failed to update localStorage for actors:', err)
  }
}





// onMounted 수정
onMounted(() => {
 try {
   // 영화 좋아요 상태 로드
   const likedMovies = JSON.parse(localStorage.getItem('likedMovies')) || []
   const likedActors = JSON.parse(localStorage.getItem('likedActors')) || []
   
   // 영화 상세 정보의 좋아요 상태 설정
   if (props.movieDetails) {
     props.movieDetails.isLiked = likedMovies.includes(props.movieDetails.id)
     props.movieDetails.is_liked = likedMovies.includes(props.movieDetails.id)
     
     // 출연 배우들의 좋아요 상태 설정
     if (props.movieDetails.actors) {
        props.movieDetails.actors = props.movieDetails.actors.map(actor => ({
          ...actor,
          isLiked: likedActors.includes(actor.id)
        }))
      }
    }

   // store의 movies 배열에서 현재 영화 찾아서 상태 동기화
   const movieInStore = store.movies.find(m => m.id === props.movieDetails.id)
   if (movieInStore) {
     props.movieDetails.is_liked = movieInStore.is_liked || likedMovies.includes(props.movieDetails.id)
     props.movieDetails.isLiked = movieInStore.isLiked || likedMovies.includes(props.movieDetails.id)
     props.movieDetails.likeCount = movieInStore.likeCount
   }
 } catch (err) {
   console.error('Failed to load liked states from localStorage:', err)
 }
})




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

button {
  margin-top: 20px;
  border-color: #F19ED2;
  color: black;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  line-height: 1.5;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #91DDCF;
}

/* 버튼 간 간격 추가 */
.button-container {
  display: flex;
  gap: 10px; /* 간격 추가 */
}

.cancel-btn {
  margin-left: 13px; /* 여백을 추가 */
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}
</style>