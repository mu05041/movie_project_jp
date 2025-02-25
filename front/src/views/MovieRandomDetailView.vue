<template>
    <div>
      <div v-if="movie" >
        <!-- 로그인 상태에 따라 다른 컴포넌트 표시 -->
        <MovieDetailInfo v-if="isLogin" :movieDetails="movie" />
        <NoLoginMovieDetail v-else :movieDetails="movie" />
      
      </div>
  
    </div>
  </template>
  
  <script setup>
  import { useMovieStore } from '@/stores/movie'
  import { onMounted, ref } from 'vue'
  import axios from 'axios'
  import MovieDetailInfo from '@/components/MovieDetailInfo.vue'
  import NoLoginMovieDetail from '@/components/NoLoginMovieDetail.vue'
  const store = useMovieStore()
  
  const movie = ref(null)
  const isLogin = store.isLogin
  
  onMounted(() => {
    axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/movies/random/`,
    })
      .then(res => {
        console.log(res.data)
        movie.value = res.data
        console.log('사탕을 눌렀어요')
      })
      .catch(err => {
        console.log(err)
      })
  })
  
  </script>
  
  <style scoped>
  
  </style>