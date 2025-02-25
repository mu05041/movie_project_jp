<template>
  <div class="login-container">
    <!-- Floating bubbles -->
    <div v-for="n in 10" :key="n" class="bubble"
      :style="{ 
        '--size': `${20 + Math.random() * 60}px`,
        '--left': `${Math.random() * 100}%`,
        '--animDuration': `${5 + Math.random() * 10}s`,
        '--delay': `-${Math.random() * 10}s`
      }">
    </div>

    <!-- Login card -->
    <div class="card">
      <h1>로그인</h1>
      <form @submit.prevent="logIn">
        <div class="form-group">
          <label for="username">사용자 이름</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder="사용자 이름을 입력하세요"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="비밀번호를 입력하세요"
            required
          />
        </div>

        <button type="submit">로그인</button>
      </form>

      <div class="signup-section">
        <p>회원이 아니신가요?</p>
        <router-link :to="{ name: 'SignUpView' }">회원가입</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMovieStore } from '@/stores/movie'

const store = useMovieStore()
const username = ref('')
const password = ref('')

const logIn = () => {
  const payload = {
    username: username.value,
    password: password.value,
  }
  store.logIn(payload)
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  /* background: linear-gradient(140deg, 
    #91DDCF 0%,
    #eceee6 35%, 
    #E8C5E5 65%,  
    #F19ED2 100%  
  );
   */
  position: relative;
  overflow: hidden;
}

.bubble {
  position: absolute;
  width: var(--size);
  height: var(--size);
  background: rgba(232, 197, 229, 0.4); 
  border-radius: 50%;
  left: var(--left);
  bottom: -20%;
  animation: float var(--animDuration) ease-in infinite;
  animation-delay: var(--delay);
  backdrop-filter: blur(2px);
  border: 1px solid rgba(145, 221, 207, 0.2); 

}

@keyframes float {
  0% {
    transform: translateY(100%) scale(1);
    opacity: 0;
  }
  50% {
    opacity: 0.8;
  }
  100% {
    transform: translateY(-100vh) scale(1.5);
    opacity: 0;
  }
}

.card {
  background: rgba(255, 233, 249, 0.4); /* F7F9F2 반투명 */
  backdrop-filter: blur(10px);
  padding: 2rem;
  border: 2px solid #91DDCF;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  animation: cardAppear 0.6s ease-out;
}

@keyframes cardAppear {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

h1 {
  color: #F19ED2;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  color: #666;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #91DDCF;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #F19ED2;
}

button {
  width: 100%;
  padding: 1rem;
  background: #91DDCF;
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.2s ease, background-color 0.3s ease;
}

button:hover {
  background: #F19ED2;
  transform: translateY(-2px);
}

.signup-section {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.signup-section p {
  color: #666;
  margin-bottom: 0.5rem;
}

a {
  color: #F19ED2;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

a:hover {
  color: #91DDCF;

}
</style>



<!-- <template>
  <div>
    <h1>LogIn Page</h1>
    <form @submit.prevent="logIn">
      <label for="username">username : </label>
      <input type="text" id="username" v-model="username"><br>

      <label for="password">password : </label>
      <input type="password" id="password" v-model="password"><br>

      <input type="submit" value="logIn">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMovieStore } from '@/stores/movie'

const store = useMovieStore()
const username = ref(null)
const password = ref(null)

const logIn = function() {
  const payload = {
    username: username.value,
    password: password.value,
  }
  store.logIn(payload)
}
</script>

<style>

</style> -->




