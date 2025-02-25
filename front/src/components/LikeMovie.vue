<template>     
  <div class="movie-card" @click="goToMovieDetail(like.id)">         
    <img :src="posterUrl" :alt="like.title" class="movie-poster">         
    <div class="movie-info">           
      <h5 class="movie-title">{{ like.title }}</h5> 
    </div>       
    <button
      @click.stop="toggleLike"
      class="btn btn-sm btn-like"
    >
      <span class="like-icon">
        {{ isLikedStatus ? '❤️' : '🤍' }}
      </span>
    </button>
  </div>   
</template>      

<script setup>   
import { useRouter } from 'vue-router';
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { computed } from 'vue';

const router = useRouter();
const store = useMovieStore();
const props = defineProps({
  like: {
    type: Object,
    required: true
  }
});

// isLiked와 is_liked 둘 다 확인하는 computed 속성
const isLikedStatus = computed(() => {
  return props.like.isLiked || props.like.is_liked || false;
});

const posterUrl = `https://image.tmdb.org/t/p/w500${props.like.poster_path}`;

const emit = defineEmits(['unliked']);

const goToMovieDetail = (movieId) => {
  router.push({
    name: 'moviedetail',
    params: { movieId: movieId.toString() }
  });
};

const toggleLike = async () => {
  try {
    const response = await axios({
      method: 'post',
      url: `${store.API_URL}/api/v1/movies/${props.like.id}/like/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    // 두 속성 모두 업데이트
    props.like.isLiked = response.data.is_liked;
    props.like.is_liked = response.data.is_liked;
    if (!response.data.is_liked) {
      emit('unliked', props.like.id);
    }

  } catch (err) {
    console.error('Failed to toggle like:', err);
  }
};
</script>


<style scoped>
.movie-card {
    background-color: white;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    border: 1px solid #eee;
    transition: all 0.2s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.movie-card:hover {
    border-color: #91DDCF;
    box-shadow: 0 2px 8px rgba(145, 221, 207, 0.2);
    transform: translateY(-5px);
}

.movie-poster {
  width: 100%;
  aspect-ratio: 2/3;
  object-fit: cover;
}

.movie-info {
    padding: 1rem;
    flex-grow: 1;
}

.movie-title {
    font-size: 1rem;
    font-weight: 600;
    color: #333;
    margin: 0;
    line-height: 1.4;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

  
button {
  margin-top: 20px;
  border-color: #F19ED2;
  color: black;
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