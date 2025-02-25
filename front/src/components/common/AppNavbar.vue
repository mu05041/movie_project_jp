<script setup>
// ... 이전 script 코드는 동일하게 유지 ...
import { RouterLink } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const searchQuery = ref('')
const store = useMovieStore()
const router = useRouter()
const isMenuOpen = ref(false)

const logOut = () => {
  store.logOut()
  isMenuOpen.value = false
}

const getUserIdAndNavigate = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/accounts/user/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then(res => {
    router.push({
      name: 'MyPageView',
      params: { id: res.data.pk }
    })
    isMenuOpen.value = false
  })
  .catch(err => {
    console.log('Error:', err)
  })
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/movies/search',
      query: { q: searchQuery.value.trim() },
    });
    searchQuery.value = '';
    isMenuOpen.value = false
  }
};

const props = defineProps({
  isDarkMode: Boolean
})

const emit = defineEmits(['toggleDarkMode'])
const toggleDarkMode = () => {
  emit('toggleDarkMode')
  console.log('다크모드 수신')
}

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}
</script>

<template>
  <nav class="navbar">
    <div class="container">
      <div class="nav-group">
        <!-- 로고 -->
        <div class="logo-container">
          <RouterLink :to="{ name:'main'}" class="logo-link">
            <img src="@/assets/로고.svg" alt="로고" class="logo">
            <img src="@/assets/텍스트로고.svg" alt="로고" class="logo">
          </RouterLink>
        </div>

        <!-- 햄버거 메뉴 버튼 -->
        <button class="menu-toggle" @click="toggleMenu" :class="{ 'is-open': isMenuOpen }">
          <span></span>
          <span></span>
          <span></span>
        </button>

        <!-- 네비게이션 메뉴 -->
        <div :class="['nav-content', { 'is-open': isMenuOpen }]">
          <div class="nav-links">
            <RouterLink :to="{ name: 'movies' }" class="nav-link" @click="isMenuOpen = false">영화조회</RouterLink>
            <RouterLink :to="{ name: 'recommend' }" class="nav-link" @click="isMenuOpen = false">영화추천</RouterLink>
            
            <template v-if="!store.token">
              <RouterLink :to="{ name: 'LogInView' }" class="nav-link" @click="isMenuOpen = false">로그인</RouterLink>
            </template>

            <template v-if="store.token">
              <button @click="logOut" class="nav-link logout-btn">로그아웃</button>
            </template>
          </div>

          <!-- 검색 및 기타 기능 -->
          <div class="right-group">
            <div class="search-container">
              <input
                v-model="searchQuery"
                @keyup.enter="handleSearch"
                class="search-input"
                placeholder="검색어를 입력하세요..."
                type="text"
              />
              <button @click="handleSearch" class="search-button">
                search
              </button>
            </div>

            <button @click="toggleDarkMode" class="darkmode-button">
              {{ isDarkMode ? '라이트모드' : '다크모드' }}
            </button>

            <template v-if="store.token">
              <button @click="getUserIdAndNavigate" class="mypage-btn">마이페이지</button>
            </template>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<style>
.navbar {
  background: var(--navbar-bg);
  padding: 0.75rem 2rem;
  border-radius: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin: 1rem auto;
  max-width: 90%;
}

.container {
  width: 100%;
}

.nav-group {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.logo-container {
  flex-shrink: 0;
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-grow: 1;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-link {
  color: #333;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  transition: all 0.3s ease;
  line-height: 1.5;
  font-size: 1rem;
}

.nav-link:hover {
  background-color: #E8C5E5;
  color: #fff;
}

.router-link-active {
  background-color: #F19ED2;
  color: #fff;
}

.right-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* 새로운 햄버거 메뉴 스타일 */
.menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 21px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 10;
}

.menu-toggle span {
  width: 100%;
  height: 3px;
  background-color: #333;
  border-radius: 10px;
  transition: all 0.3s linear;
  position: relative;
  transform-origin: 1px;
}

.menu-toggle.is-open span:first-child {
  transform: rotate(45deg);
}

.menu-toggle.is-open span:nth-child(2) {
  opacity: 0;
  transform: translateX(20px);
}

.menu-toggle.is-open span:nth-child(3) {
  transform: rotate(-45deg);
}

/* 반응형 스타일 */
@media (max-width: 1024px) {
  .menu-toggle {
    display: flex;
  }

  .nav-content {
    display: none;
    width: 100%;
    flex-direction: column;
    gap: 1rem;
    padding-top: 1rem;
  }

  .nav-content.is-open {
    display: flex;
  }

  .nav-links {
    flex-direction: column;
    width: 100%;
  }

  .right-group {
    flex-direction: column;
    width: 100%;
  }

  .nav-link,
  .darkmode-button,
  .mypage-btn {
    width: 100%;
    text-align: center;
  }
}

/* 기존 스타일 유지 */
.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #E8C5E5;
}

.mypage-btn {
  background-color: #F19ED2;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  line-height: 1.5;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mypage-btn:hover {
  background-color: #E8C5E5;
  transform: scale(1.05);
}

/* 검색창 원래 스타일로 복원 */
.search-input {
  border-radius: 10px;
  overflow: hidden;
  border: #F19ED2;
  background-color: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.search-button {
  background-color: #F19ED2;
  border-radius: 20px;
  border: #F19ED2;
}

.darkmode-button {
  background-color: var(--darkmode-button-bg);
  border-radius: 20px;
  border: #F19ED2;
  font-size: 1rem;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  margin-right: 20px;
  background: none !important;
  gap: 8px;
}

.logo {
  height: 20px;
  width: auto;
}

.logo-link:hover {
  background: none !important;
  transform: none !important;
}
</style>