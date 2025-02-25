<template>
  <div class="reviews-container">
    <h4 class="reviews-title">사용자 평</h4>
    <div class="reviews-list">
      <div v-for="review in store.reviews" 
           :key="review.id" 
           class="review-box">
        <div class="review-header">
          <RouterLink
            :to="{ name:'MyPageView', params: { id: review.user }}"
            class="username-link">
            {{ review.user_username }}
          </RouterLink>
        </div>
        <!-- 리뷰 세부 조회 모달 -->
        <div 
          id="modalOpenButton" 
          @click="openReviewModal(review)"
          class="review-content" 
        >
        <div class="star-rating">
          <span 
            v-for="n in 5" 
            :key="n" 
            class="star"
            :class="{ 'filled': n <= review.rating }">
            ★
          </span>
        </div>
        {{ review.content }}
      </div>
    </div>
  </div>

        <!-- 리뷰 모달 -->
        <div v-if="isReviewModalOpen" class="modal"  @click="closeReviewModalOnClickOutside">
          <div class="modal-content">
            <ReviewDetailView 
              :review="selectedReview"
              :closeReviewModal="closeReviewModal" 
              :onReviewSubmitted="onReviewSubmitted" 
            />
          </div>
        </div>
  </div>
</template>


<script setup>
import ReviewDetailView from './ReviewDetailView.vue'
import { RouterLink } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const store = useMovieStore()
const route = useRoute()
const movieId = route.params.movieId
const router = useRouter()


// 리뷰 작성 모달 상태
const isReviewModalOpen = ref(false);

// 선택된 리뷰
const selectedReview = ref(null);

// 리뷰 모달 열기/닫기 메서드
const openReviewModal = (review) => {
  isReviewModalOpen.value = true;
  selectedReview.value = review; // 선택된 리뷰 저장
  console.log('리뷰 모달이 열렸습니다.')
};

const closeReviewModal = () => {
  isReviewModalOpen.value = false;
  router.push({ name: 'moviedetail' })
};

onMounted(() => {
  console.log('리뷰 불러왔습니다.')
  store.getReviewList(movieId)
})

// 모달 외부 클릭 시 닫기
const closeReviewModalOnClickOutside = (event) => {
  if (event.target.classList.contains('modal')) {
    closeReviewModal();
  }
};

// 리뷰 제출 후 페이지 새로고침 및 moviedetail로 이동
const onReviewSubmitted = () => {
  // 페이지 새로고침 및 moviedetail로 이동
  window.location.reload();
  router.push({ name: 'moviedetail' });
};
</script>

<style scoped>

.reviews-container {
  padding: 20px;
  border-radius: 20px;
}

.reviews-title {
  margin-bottom: 20px;
  font-size: 1.5rem;
  font-weight: bold;
  color: #6bc0b0;
  text-align: center;
}

.reviews-list {
  display: grid;
  gap: 15px;
}

.review-box {
  background-color: var(--review-box-bg);
  border-radius: 15px;
  padding: 15px;
  border: 2px solid #91DDCF;
  box-shadow: 0 2px 8px rgba(145, 221, 207, 0.2);
  transition: all 0.2s ease;
}

.review-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(145, 221, 207, 0.3);
  border-color: #F19ED2;
}

.review-header {
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid #E8C5E5;
}

.username-link {
  color: #91DDCF;
  font-weight: bold;
  text-decoration: none;
  transition: color 0.2s ease;
}

.username-link:hover {
  color: #F19ED2;
}

.review-content {
  color: #4a4a4a;
  text-decoration: none;
  display: block;
  line-height: 1.5;
  transition: color 0.2s ease;
}

.review-content:hover {
  color: #E8C5E5;
}


/* 리뷰 별점 스타일변경*/
.star-rating {
  display: inline-flex;
  align-items: center;
  margin-right: 8px;
}

.star {
  font-size: 1.2em;
  color: #ddd;
  transition: color 0.2s;
}

.star.filled {
  color: #ffd700;
}

.rating-number {
  margin-left: 4px;
  font-size: 0.9em;
  color: #666;
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

  