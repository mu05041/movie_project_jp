<template>
  <div class="col-md-4 col-lg-3 col-xl-2 mb-4">
    <div class="">
      <img :src="posterUrl" alt="Movie Poster" class="card-img-top">
      <div class="card-body d-flex flex-column">
        <!-- <h5 class="card-title">{{ movie.title }}</h5> -->
        <br>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  movie: Object
})
// 포스터 URL을 동적으로 생성
const posterUrl = `https://image.tmdb.org/t/p/w500${props.movie.poster_path}`
</script>

<style scoped>
.card {
  border: none;
  background-color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 100%;
}

.card-img-top {
  object-fit: cover;
  width: 100%;
  height: 250px;  /* 카드 이미지의 높이를 설정 */
  border-radius: 8px 8px 0 0; /* 이미지의 상단 모서리 라운드 처리 */
}

.card-body {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin-bottom: 8px;
}

.card-text {
  font-size: 0.9rem;
  color: #777;
  line-height: 1.4;
  text-align: center;
  margin-bottom: auto;
}

/* 카드 hover 효과 */
.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.card:hover .card-img-top {
  transform: scale(1.05); /* 이미지 크기 살짝 확대 */
}

/* 반응형 개선 */
@media (max-width: 768px) {
  .card-img-top {
    height: 220px;
  }
}

@media (max-width: 576px) {
  .card-img-top {
    height: 180px;
  }
}
</style>
