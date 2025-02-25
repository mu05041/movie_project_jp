<template>
  <div class="container mt-5">
    <h2>당신만의 {{ movieTitle }}, </h2>
    <h3>영화의 끝을 리뷰로 이어가세요!</h3> 
    <form @submit.prevent="submitReview">
      <!-- 리뷰 내용 -->
      <div class="mb-3">
        <label for="content" class="form-label">리뷰 내용</label>
        <textarea
          id="content"
          v-model="content"
          class="form-control"
          rows="5"
          placeholder="리뷰를 작성해 주세요"
          @keydown.enter="submitReviewAndCloseModal"
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
      <button type="submit">제출</button>
    </form>
  </div>
</template>

<script setup>
// ReviewForm 컴포넌트
import { ref } from 'vue';
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';

// 부모 컴포넌트에서 전달받은 closeReviewModal 메서드
const props = defineProps({
  closeReviewModal: Function,
  movieId: Number,
  onReviewSubmitted: Function, // 부모에서 전달받을 콜백 함수
});

const content = ref('');
const rating = ref(null);
const store = useMovieStore()
const movieTitle = ref('');

const fetchMovieTitle = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/${props.movieId}/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((res) => {
      movieTitle.value = res.data.title
    })
    .catch((err) => {
      console.log(err);
    });
};

// 컴포넌트가 로드될 때 영화 제목을 가져오기
fetchMovieTitle();


// 리뷰 제출 함수
const submitReview = () => {
  if (content.value && rating.value) {
    axios({
      method: 'post',
      url: `${store.API_URL}/api/v1/movies/${props.movieId}/reviews/`,
      data: {
        content: content.value,
        rating: rating.value
      },
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then(() => {
        props.onReviewSubmitted(); // 부모에서 정의한 콜백 호출
        // 부모에게 리뷰 제출 완료 이벤트 전달
        props.closeReviewModal(); // 모달 닫기
        rating.value = ''
        content.value = ''
      })
      .catch((err) => {
        console.log(err);
      });
  } else {
    alert('리뷰 내용을 입력하고 평점을 선택하세요.');
  }
};

// Enter키를 눌렀을 때 리뷰 제출 후 모달 닫기
const submitReviewAndCloseModal = (event) => {
  event.preventDefault(); // 기본 Enter 동작 방지 (폼 제출)
  submitReview();
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
