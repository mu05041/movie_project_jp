<template>
  <div class="col-md-4 col-lg-3 col-xl-2 mb-4">
    <div class="movie-card h-100">
      <img :src="posterUrl" alt="Movie Poster" class="card-img-top">
      <div class="card-body d-flex flex-column">
        <h5 class="card-title">{{ movie.title }}</h5>
   
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


.card-img-top {
  object-fit: cover;
  width: 100%;
  object-fit: contain;  /* 카드 이미지의 높이를 설정 */
  border-radius: 8px 8px 0 0; /* 이미지의 상단 모서리 라운드 처리 */
}

.card-body {
  padding: 1.25rem;

}

.card-title {
  font-size: 1.2rem;
  font-weight: bold;
}

.card-text {
  font-size: 1rem;
  color: #555;
}

/* 카드 hover 효과 */
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}


</style>

