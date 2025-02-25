<template>
  <div class="container mt-5">
    <div v-if="review" class="card shadow-sm p-4">
      <h2 class="text-center mb-4">{{ review.movie_title }} 리뷰</h2>
      <div class="card-body">
        <h3 class="card-title">
          작성자:
          <RouterLink  
            v-if="review.user" 
            :to="{ name: 'MyPageView', params: { id: review.user }}"
          >
              {{ review.user_username }}
          </RouterLink>
        </h3>
        <p class="card-text">{{ review.content }}</p>
      </div>
      <div class="d-flex justify-content-center gap-3 mt-4">
        <button class="px-4 update-btn" @click="goToUpdateReview">
          리뷰 수정
        </button>
        <button class="px-4 delete-btn" @click="deleteReview">
          리뷰 삭제
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useRouter } from 'vue-router'

const route = useRoute()
const store = useMovieStore()
const reviewId = route.params.reviewId

const router = useRouter()

const props = defineProps({
  review: Object,
  closeReviewModal: Function,
  onReviewSubmitted: Function,
})


// 리뷰 수정 페이지로 이동
const goToUpdateReview = function () {
  console.log(props.review)
  console.log(props.review.user_username)
  const movieId = props.review.movie_id
  router.push({ name: 'updateReview', params: { reviewId: props.review.id, movieId: props.review.movieId } })

 
}

// 리뷰 삭제
const deleteReview = function () {
  axios({
    method: 'delete',
    url: `${store.API_URL}/api/v1/reviews/${props.review.id}/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(res => {
        console.log('리뷰 삭제 완료:', res.data)
        const movieId = props.review.movie_id
        props.closeReviewModal()
        // 페이지 새로 고침 (리뷰 삭제 후 해당 영화 상세 페이지로 리다이렉트)
        router.push({ name: 'moviedetail', params: { movieId: movieId } }).then(() => {
          // 페이지 새로 고침
          window.location.reload()
      })
    })
    .catch(err => {
      console.log(err)
    })
}
</script>

<style scoped>
h2 {
  color: #333;
}

.card {
  background-color: var(--profile-info-bg);
  max-width: 600px;
  margin: 0 auto;
  border-radius: 10px;
  border-color:#F19ED2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.);

}

.card-title {
  font-size: 1.5rem;
  color: #444;
}

.card-text {
  font-size: 1.1rem;
  line-height: 1.5;
  color: #333;
}

.d-flex {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
}

.alert {
  text-align: center;
}

button {
  margin-top: 20px;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  line-height: 1.5;
  font-size: 1rem;
  cursor: pointer;
  border: none;
  outline: none;
}

/* 수정 버튼 스타일 */
.update-btn {
  background-color: #91DDCF; /* 크림색 */
  border-color: #f6ffd0;
}

.update-btn:hover {
  background-color: #F19ED2;
}

/* 삭제 버튼 스타일 */
.delete-btn {
  background-color: #F19ED2;
  border-color: #F19ED2;
  color: black;
}

.delete-btn:hover {
  background-color: #91DDCF;
}
</style>
