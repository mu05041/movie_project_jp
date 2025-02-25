<template>     
  <div class="img-container">
    <img 
      :src="`https://image.tmdb.org/t/p/w500${like.profile_path}`"
      alt="profile"
      class="actor-image">
  </div>
  <p class="actor-name">{{ like.name }}</p>      
</template>      

<script setup>   
import { useRouter } from 'vue-router';
const router = useRouter();

const props = defineProps({     
  like: Object   
})   



</script>      

<style scoped>

</style>