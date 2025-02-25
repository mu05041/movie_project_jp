<template>
  <div class="profile-container">
      <div class="profile-info">
          <h1>{{ username }}의 프로필</h1>

           <button @click="handleFollow">
              {{ isFollowed ? '언팔로우' : '팔로우' }}
          </button>

          <div class="follow-stats">
              <div class="stat-item">
                  <p class="stat-label">팔로워</p>
                  <p class="stat-value">{{ followersCount }}</p>
              </div>
              <div class="stat-item">
                  <p class="stat-label">팔로잉</p>
                  <p class="stat-value">{{ followingsCount }}</p>
              </div>
          </div>
      </div>

      <div class="content-section">
          <div class="reviews-section">
              <h3>작성한 리뷰</h3>
              <div v-if="userReviews.length">
                  <div v-for="review in userReviews" 
                       :key="review.id"
                       @click="goToMovieDetail(review.movie_id)"
                       class="review-item">
                      <p>{{ review.movie_title }} - {{ review.rating }}점 {{ review.content }}</p>
                  </div>
              </div>
          </div>

          <div class="liked-section">
              <h3>내가 좋아요한 영화</h3>
              <div v-if="likedMovies.length" class="liked-movies-grid">
                  <div v-for="like in likedMovies" 
                       :key="like.id"
                       class="liked-movie-wrapper">
                      <LikeMovie :like="like"/>
                  </div>
              </div>
          </div>


          <div class="liked-actor">
            <h3>내가 좋아요한 배우</h3>
            <div class="actors-grid"> <!-- 이 class만 추가 -->
              <div v-for="like in likedActors"
                  :key="like.id"
                  class="actor-item">
                <LikeActor :like="like"/>
              </div>
            </div>
          </div>
      </div>
  </div>
</template>  
<script setup>
import { useMovieStore } from '@/stores/movie'
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import axios from 'axios'
import LikeMovie from '@/components/LikeMovie.vue';
import LikeActor from '@/components/LikeActor.vue';
const store = useMovieStore()
const route = useRoute()
const router = useRouter()

// 상태 관리
const user = ref({}); // 사용자 데이터를 저장할 반응형 변수
const username = ref('')
const isFollowed = ref(false)
const followersCount = ref(0)
const followingsCount = ref(0)
const userReviews = ref([])
const likedMovies = ref([])
const likedActors = ref([])

// 프로필 정보 가져오기
const getProfileData = () => {
  console.log('Route params:', route.params.id)  // URL 파라미터 로깅 추가
  axios({
    method: 'get',
    url: `${store.API_URL}/accounts/${route.params.id}/`,  
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then(res => {
    username.value = res.data.username
    console.log(res.data)
    isFollowed.value = res.data.is_followed
    followersCount.value = res.data.followers_count
    followingsCount.value = res.data.followings_count
  })
  .catch(err => {
    console.log('Profile error:', err.response)
  })
}

// 팔로우/언팔로우 처리
const handleFollow = () => {
  axios({
    method: 'post',
    url: `${store.API_URL}/accounts/${route.params.id}/follow/`,
    headers: {
      Authorization: `Token ${store.token}` // localStorage 대신 store의 token 사용
    }
  })
    .then(res => {
      isFollowed.value = res.data.is_followed
      followersCount.value = res.data.followers_count
      followingsCount.value = res.data.followings_count
    })
    .catch(err => {
      console.log('Follow error:', err.response) // 자세한 에러 로깅
      if (err.response?.status === 401) {
        console.log('Token:', store.token) // 토큰 값 확인
      }
    })
}


// 사용자의 리뷰 목록 가져오기
const getUserReviews = () => {
  console.log('Requesting reviews with token:', store.token)
  axios({
    method: 'get',
    url: `${store.API_URL}/accounts/${route.params.id}/reviews/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then(res => {
    console.log(res.data)
    userReviews.value = res.data
    console.log(route.params.id)
  })
  .catch(err => {
    console.log('Reviews error:', err.response)
  })
}

onBeforeRouteUpdate((to, from) => {
  userId.value = to.params.id
})

// 좋아요한 영화 목록 가져오기
const getLikedMovies = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/accounts/${route.params.id}/liked-movies/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then(res => {
    console.log('likedata=',res.data)
    likedMovies.value = res.data
    store.updateLocalStorage(likedMovies)
    })
  .catch(err => {
    console.log('Liked movies error:', err.response)
  })
}


// 좋아요한 배우 목록 가져오기
const getLikedActors = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/accounts/${route.params.id}/liked-actors/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then(res => {
    console.log('likedata=',res.data)
    likedActors.value = res.data
    console.log(likedActors)
  })
  .catch(err => {
    console.log('Liked actors error:', err.response)
  })
}


// 영화 상세페이지로 이동하기
const goToMovieDetail = (movieId) => {
    router.push({
        name: 'moviedetail',
        params: { movieId: movieId.toString() }
    })
}


onMounted(() => {
  getProfileData()
  getUserReviews()
  getLikedMovies()
  getLikedActors()
})

</script>
<style scoped>
.profile-container {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 2rem;
    min-height: 100vh;
    /* background-color: #F7F9F2; */
    padding: 2rem;
}

.profile-info {
    background-color: var(--profile-info-bg);
    padding: 2rem;
    border-radius: 12px;
    height: fit-content;
    position: sticky;
    top: 2rem;
}

.profile-info h1 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #333;
    margin-bottom: 1.5rem;
}

button {
    width: 100%;
    background-color: #91DDCF;
    /* color: white; */
    border: none;
    padding: 0.75rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
    margin-bottom: 1.5rem;
}

button:hover {
    background-color: #E8C5E5;
}

.follow-stats {
    border-top: 1px solid #eee;
    padding-top: 1.5rem;
}

.stat-item {
    margin-bottom: 1rem;
    text-align: center;
    padding: 1rem;
    background-color: var(--profile-info-bg);
    border-radius: 8px;
}

.stat-label {
    font-size: 0.9rem;
    color: var(--stat-label-color);
    margin-bottom: 0.5rem;
}

.stat-value {
    font-size: 1.25rem;
    font-weight: 600;
    color: #91DDCF;
}

.content-section {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.reviews-section, .liked-section {
    background-color: var(--profile-info-bg);
    padding: 2rem;
    border-radius: 12px;
}

.reviews-section h3, .liked-section h3 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #F19ED2;
}

.review-item {
    padding: 1.25rem;
    border-radius: 8px;
    background-color: var(--profile-info-bg);;
    margin-bottom: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid #eee;
}

.review-item:hover {
    border-color: #91DDCF;
    box-shadow: 0 2px 8px rgba(145, 221, 207, 0.2);
}

.review-item p {
    color: #333;
    line-height: 1.6;
}

.liked-movies-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-top: 1rem;
}

.liked-movie-wrapper {
    height: 100%;
}

.liked-actors-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-top: 1rem;
}

.liked-actor-wrapper {
    height: 100%;
}


@media (max-width: 768px) {
    .profile-container {
        grid-template-columns: 1fr;
        padding: 1rem;
    }

    .profile-info {
        position: static;
        margin-bottom: 1rem;
    }

    .liked-movies-grid {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 1rem;
    }
}


/* 배우 이미지  */


.actors-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.liked-actor {
  background-color: var(--profile-info-bg);
  padding: 2rem;
  border-radius: 12px;
}

.liked-actor h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #F19ED2;
}

/* 이 부분이 핵심입니다 */
.actor-item :deep(.img-container) {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
}

.actor-item :deep(.actor-image) {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.actor-item :deep(.actor-name) {
  margin-top: 8px;
  text-align: center;
  font-size: 0.9rem;
}

</style>
