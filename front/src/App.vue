<script setup>
import AppNavbar from './components/common/AppNavbar.vue'
import { useRoute,useRouter  } from 'vue-router';
import { ref,onMounted, watch } from 'vue'
import '@/assets/darkmode.css'  // 다크모드 스타일 import
import Footer from '@/components/Footer.vue'; // Footer 컴포넌트 import

const route = useRoute()
const router = useRouter();

//다크모드 토글
const isDarkMode = ref(false)
const toggleDarkMode = () =>{
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

//다크모드 상태저장
watch(isDarkMode, (newValue) => {
  localStorage.setItem('darkMode', newValue)
})

// 페이지 로드 시 저장된 상태 복원
onMounted(() => {
  const savedDarkMode = localStorage.getItem('darkMode')
  if (savedDarkMode !== null) {
    isDarkMode.value = savedDarkMode === 'true'
    // 초기 로드 시에도 dark 클래스 적용
    if (isDarkMode.value) {
      document.documentElement.classList.add('dark')
    }
  }
})

//챗봇으로 이동
const navigateToChatbot = () => {
  console.log('챗봇이동')
  router.push('/chat');
};


</script>

<template>
  <div :class="{ 'dark': isDarkMode }">
      <div class="ibm-plex-sans-kr-regular main-container">

          <AppNavbar 
          :isDarkMode="isDarkMode"
          @toggleDarkMode="toggleDarkMode"
          />

        <!-- <AppNavbar
        v-if="!route.meta.hideNavbar"
        /> -->
        <RouterView />
        <button
        class="chat-button"
        @click="navigateToChatbot"
        >
        <img src="@/assets/GPT로고.svg" class="chat-icon">
      
      </button>

    </div>
    <Footer />
  </div>
</template>

<style>
/* 컬러팔레트 https://colorpalettes.net/color-palette-4539/ */

/* 구글font import */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400&display=swap');



/* 글꼴 */
html, body {
  font-family: "IBM Plex Sans KR", sans-serif;
  font-weight: 400;
  font-style: normal;
}

.ibm-plex-sans-kr-regular {
  font-family: "IBM Plex Sans KR", sans-serif;
  font-weight: 400;
  font-style: normal;
}

/* 배경 이미지 설정 */
.main-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  background: var(--bg-gradient);
  /* background: linear-gradient(156deg, rgba(255,255,255,1) 35%, rgba(168,237,234,1) 66%, rgba(254,214,227,1) 93%); */
  /* background: linear-gradient(to top, transparent, rgb(255, 255, 255, 0.8)),
  url("./assets/aaa.jpg"); */
  /* background-size: cover;  
  background-repeat: no-repeat;  
  background-attachment: fixed; */
}


/* curosr change*/
/*
*{
  cursor : url('@/assets/로고.svg') 2 2, auto;}
*:active{
  cursor : url('@/assets/로고.svg') 2 2, auto;}
*/
.chat-button {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  width: 3.5rem;
  height: 3.5rem;
  background: linear-gradient(to right, #a8edea, #fed6e3);
  color: black;
  border-radius: 9999px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 50;
  border: none;
  cursor: pointer;
}

.chat-button:hover {
  background: linear-gradient(to right, #89e5e1, #ffc4d7);
  transform: scale(1.05);
}
.chat-icon {
  width: 2rem;
  height: 2rem;
}


</style>
