import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const movies = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const router = useRouter()
  const reviews = ref([])
  const username = ref(null)

  // 모달 상태 추가
  const isModalOpen = ref(false)
  const searchQuery = ref('') // 검색어 상태

  // 모달 열기
  const openModal = () => {
    isModalOpen.value = true
  }

  // 모달 닫기
  const closeModal = () => {
    isModalOpen.value = false
  }

  // DRF로 전체 게시글 요청을 보내고 응답을 받아 movies에 저장하는 함수
  const getMovieLists = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movies/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        console.log(res.data)
        movies.value = res.data
        // 로컬 스토리지에서 좋아요 상태를 불러와서 적용
        loadLikedMovies()
      })

      .catch((err) => {
        console.log(err)
      })
  }

  // 로컬 스토리지에서 좋아요 상태 불러오기
  const loadLikedMovies = () => {
    const likedMovies = JSON.parse(localStorage.getItem('likedMovies')) || []
    movies.value.forEach((movie) => {
      if (likedMovies.includes(movie.id)) {
        movie.isLiked = true
      }
    })
  }

  // 좋아요 상태를 로컬 스토리지에 저장하는 함수
  const updateLocalStorage = (movie) => {
    const likedMovies = JSON.parse(localStorage.getItem('likedMovies')) || []
    if (movie.isLiked) {
      likedMovies.push(movie.id)
    } else {
      const index = likedMovies.indexOf(movie.id)
      if (index > -1) {
        likedMovies.splice(index, 1)
      }
    }
    localStorage.setItem('likedMovies', JSON.stringify(likedMovies))
  }

  // 로그인 및 회원가입 관련 함수들
  const signUp = function({ username, password1, password2 }) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username,
        password1,
        password2,
      }
    })
      .then(res => {
        console.log(res.data)
        const password = password1
        logIn({ username, password })
      })
      .catch(err => console.log(err))
  }

  const logIn = function({ username, password }) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username,
        password,
      }
    })
      .then(res => {
        console.log(res.data)
        token.value = res.data.key
        username = username
        console.log(username)
        router.push({ name: 'main' })
      })
      .catch(err => console.log(err))
  }

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        console.log(res.data)
        token.value = null
        router.push({ name: 'main' })
      })
      .catch(err => console.log(err))
  }

  // 리뷰 데이터들
  const getReviewList = function (movieId) {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movies/${movieId}/reviews/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        console.log(res.data) // 서버에서 받은 리뷰 목록 출력
        reviews.value = res.data // reviews 상태에 리뷰 목록 저장
      })
      .catch((err) => {
        console.log(err) // 오류 처리
      })
  }

  return { 
    movies, 
    API_URL, 
    getMovieLists, 
    signUp, 
    logIn, 
    token, 
    isLogin, 
    logOut, 
    getReviewList, 
    reviews,
    updateLocalStorage, // store에서 updateLocalStorage 함수 제공
    isModalOpen,
    openModal,
    closeModal, 
    searchQuery,
    username
  }
}, { persist: true })
