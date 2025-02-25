import { createRouter, createWebHistory } from 'vue-router'
import MovieListView from '@/views/MovieListView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import MainPageView from '@/views/MainPageView.vue'

import { useMovieStore } from '@/stores/movie'
import ReviewListView from '@/views/ReviewListView.vue'
import ReviewDetailView from '@/views/ReviewDetailView.vue'
import ReviewForm from '@/components/ReviewForm.vue'
import MyPageView from '@/views/MyPageView.vue'
import UpdateReviewForm from '@/components/UpdateReviewForm.vue'
import TodayMovie from '@/views/TodayMovie.vue'
import SearchView from '@/views/SearchView.vue'
import RecommendView from '@/views/RecommendView.vue'
import ChatBot from '@/components/ChatBot.vue'
import MovieRandomDetailView from '@/views/MovieRandomDetailView.vue'
import RollingCandy from '@/views/RollingCandy.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      name: 'main',
      component: MainPageView,
      meta:{ hideNavbar: true}
    },
    {
      path: '/movies',
      name: 'movies',
      component: MovieListView
    },
    {
      path: '/movies/:movieId',
      name: 'moviedetail',
      component: MovieDetailView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/movies/:movieId/reviews',
      name: 'ReviewList',
      component: ReviewListView
    },
    {
      path: '/reviews/:reviewId',
      name: 'ReviewDetail',
      component: ReviewDetailView
    },
    {
      path: '/movies/:movieId/review',
      name: 'ReviewForm',
      component: ReviewForm
    },
    {
      path: '/reviews/:reviewId/update/:movieId',
      name: 'updateReview',
      component: UpdateReviewForm
    },
    {
      path: '/profile/:id',
      name: 'MyPageView',
      component: MyPageView
    },
    {
      path: '/movies/recommend',
      name: 'recommend',
      component: RecommendView
    },
    {
      path: '/movies/today',
      name: 'TodayMovie',
      component: TodayMovie
    },
    {
      path: '/movies/search',
      name: 'SearchView',
      component: () => import('@/views/SearchView.vue'), 
    },
    {
      path: '/chat',
      name: 'ChatBot',
      component: ChatBot
    },
    {
      path: '/movies/random',
      name: 'movierandom',
      component: MovieRandomDetailView
    },
    {
      path: '/movies/candy',
      name: 'candy',
      component: RollingCandy
    },
  ],
})

router.beforeEach((to, from) => {
  const store = useMovieStore()
  if((to.name === 'movies' || to.name === 'recommend') && !store.isLogin) {
    alert('로그인이 필요합니다.')
    return { name: 'LogInView'}
  }
  if((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin)){
    alert('이미 로그인이 되어 있습니다.')
    return { name: 'main'}
  }
})

export default router
