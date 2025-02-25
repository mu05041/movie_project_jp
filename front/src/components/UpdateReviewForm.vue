<template>
  <div class="container mt-5">
    <h2>{{ reviewId ? '리뷰 수정' : '리뷰 작성' }}</h2>
    <form @submit.prevent="updatesubmitReview">
      <!-- 리뷰 내용 -->
      <div class="mb-3">
        <label for="content" class="form-label">리뷰 내용</label>
        <textarea
          id="content"
          v-model="content"
          class="form-control"
          rows="5"
          placeholder="리뷰를 작성해 주세요"
        ></textarea>
      </div>

      <!-- 평점 -->
      <div class="mb-3">
        <label for="rating" class="form-label">평점</label>
        <div>
          <input
            type="radio"
            id="rating1"
            value="1"
            v-model="rating"
            class="form-check-input"
          />
          <label for="rating1" class="form-check-label">1점</label>

          <input
            type="radio"
            id="rating2"
            value="2"
            v-model="rating"
            class="form-check-input ms-3"
          />
          <label for="rating2" class="form-check-label">2점</label>

          <input
            type="radio"
            id="rating3"
            value="3"
            v-model="rating"
            class="form-check-input ms-3"
          />
          <label for="rating3" class="form-check-label">3점</label>

          <input
            type="radio"
            id="rating4"
            value="4"
            v-model="rating"
            class="form-check-input ms-3"
          />
          <label for="rating4" class="form-check-label">4점</label>

          <input
            type="radio"
            id="rating5"
            value="5"
            v-model="rating"
            class="form-check-input ms-3"
          />
          <label for="rating5" class="form-check-label">5점</label>
        </div>
      </div>

      <!-- 제출 버튼 -->
      <button type="submit" class="btn btn-primary">제출</button>
    </form>

    <!-- 제출된 리뷰 출력 (디버깅용) -->
    <div v-if="submitted">
      <h3 class="mt-4">제출된 리뷰</h3>
      <p><strong>내용:</strong> {{ content }}</p>
      <p><strong>평점:</strong> {{ rating }}점</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useMovieStore } from '@/stores/movie';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const content = ref('');
const rating = ref(null);
const submitted = ref(false);
const reviewId = ref(null); // 리뷰 ID
const route = useRoute();
const router = useRouter();
const store = useMovieStore();


// 리뷰 수정 페이지라면, 기존 리뷰 데이터를 불러오기
onMounted(() => {
  if (route.params.reviewId) {
    reviewId.value = route.params.reviewId;
    // 기존 리뷰 데이터 불러오기
    axios.get(`${store.API_URL}/api/v1/reviews/${reviewId.value}/`)
      .then(res => {
        content.value = res.data.content;
        rating.value = res.data.rating;
      })
      .catch(err => {
        console.log(err);
      });
  }
});

// 리뷰 작성/수정 처리 함수
const updatesubmitReview = () => {
  if (content.value && rating.value) {
    submitted.value = true;

    const reviewData = {
      content: content.value,
      rating: rating.value,
    };

  
    if (reviewId.value) {
      // 리뷰 수정
      axios.put(`${store.API_URL}/api/v1/reviews/${reviewId.value}/`, reviewData, {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      })
        .then(() => {
          router.push({ name: 'moviedetail', params: { movieId: route.params.movieId } }).then(() => {
            window.location.reload(); // 새로 고침
          });
        })
        .catch(err => {
          console.log(err);
        });
    } else {
      // 리뷰 작성
      axios.post(`${store.API_URL}/api/v1/movies/${route.params.movieId}/reviews/`, reviewData, {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      })
        .then(() => {
          
          router.push({ name: 'moviedetail' });
        })
        .catch(err => {
          console.log(err);
        });
    }
  } else {
    alert('리뷰 내용을 입력하고 평점을 선택하세요.');
  }
};

</script>

<style scoped>
button {
  margin-top: 20px;
  background-color: #F19ED2;
  border:none;
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

</style>
