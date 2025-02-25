<template>
  <div v-if="isModalOpen" class="modal-backdrop" @click="closeModal">
    <div class="modal-content" @click.stop>
      <h2 class="text-center mb-4">영화 검색</h2>
      <div class="card shadow-sm">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <input
              type="text"
              v-model="searchQuery"
              class="form-control form-control-lg"
              placeholder="검색어를 입력하세요."
              @keyup.enter="searchMovies"
            />
            <button
              @click="searchMovies"
              class="btn btn-primary btn-lg ms-2"
            >
              검색
            </button>
          </div>
          <div v-if="loading" class="text-center text-muted">검색 중...</div>
          <div v-if="error" class="alert alert-danger" role="alert">
            {{ error }}
          </div>
          <div v-if="movies.length === 0 && !loading && !error" class="text-center">
            검색 결과가 없습니다.
          </div>
          <ul v-if="movies.length > 0" class="list-group mt-3">
            <li v-for="movie in movies" :key="movie.id" class="list-group-item d-flex justify-content-between align-items-center">
              <RouterLink
                :to="{ name: 'moviedetail', params: { movieId: movie.id }}"
                class="text-decoration-none"
              >
                {{ movie.title }}
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>
      <button class="close-modal" @click="closeModal">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "axios";
import { useMovieStore } from "@/stores/movie";
import { RouterLink, useRoute } from 'vue-router'

// Store 가져오기
const store = useMovieStore();

// 상태 관리
const searchQuery = ref(""); // 검색어
const movies = ref([]); // 영화 데이터
const loading = ref(false); // 로딩 상태
const error = ref(null); // 에러 메시지
const route = useRoute()
const isModalOpen = ref(true); // 모달 열기 상태

// 영화 검색 함수
const searchMovies = async () => {
  loading.value = true; // 로딩 시작
  error.value = null; // 에러 초기화
  movies.value = []; // 이전 검색 결과 초기화

  if (!searchQuery.value.trim()) {
    error.value = "검색어를 입력해주세요.";
    loading.value = false;
    return;
  }

  try {
    const response = await axios.get(`${store.API_URL}/api/v1/movies/search/`, {
      params: { search: searchQuery.value }, // 검색어 전달
    });
    movies.value = response.data; // 검색 결과 저장
  } catch (err) {
    if (err.response?.status === 400) {
      error.value = "검색어를 입력해주세요.";
    } else if (err.response?.status === 404) {
      error.value = `'${searchQuery.value}'에 대한 검색 결과가 없습니다.`;
    } else {
      error.value = "검색 중 문제가 발생했습니다.";
    }
  } finally {
    loading.value = false; // 로딩 종료
  }
};

// URL 쿼리 파라미터 감지
watch(
  () => route.query.q,
  (newQuery) => {
    if (newQuery) {
      searchQuery.value = newQuery;
      searchMovies(newQuery);
    }
  },
  { immediate: true }
);

// 모달 닫기 함수
const closeModal = () => {
  isModalOpen.value = false;
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  width: 80%;
  max-width: 600px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

button.close-modal {
  background-color: transparent;
  border: none;
  color: #007bff;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 10px;
}

button.close-modal:hover {
  text-decoration: underline;
}

.card {
  border-radius: 10px;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.3); /* 투명한 화이트 배경 */
  backdrop-filter: blur(10px); /* 블러 효과 추가 */
}

.card-body {
  padding: 30px;
}

button {
  background: linear-gradient(45deg, #cffae2, #ee98ce);
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  line-height: 1.5;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 10rem;
  height: 3rem;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
  background: linear-gradient(45deg, #fbc2eb, #a6c1ee);
}

button:active {
  transform: translateY(0);
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.2);
}

button:focus {
  outline: none;
}

.list-group {
  display: flex;
  flex-direction: column;
  gap: 1rem; /* 검색 결과 간격 조정 */
}

.list-group-item {
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: background-color 0.2s;
  background-color: rgba(255, 255, 255, 0.3); /* 리스트 아이템도 약간 투명하게 */
}

.list-group-item:hover {
  background-color: rgba(248, 249, 250, 0.95);
}

.alert {
  margin-top: 20px;
  font-size: 16px;
}

.form-control {
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

</style>
