<!-- CandyAnimation.vue -->
<template>
  <div class="candy-container">
    <TransitionGroup name="fall">
      <div
        v-for="candy in candies"
        :key="candy.id"
        class="candy"
        :style="getCandyStyle(candy)"
      >
        <img :src="candy.icon" width="32" height="32" />
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
// 아이콘 import
import 젤리Icon from '@/assets/icons/젤리.png'
import 초콜릿Icon from '@/assets/icons/초콜릿.png'
import 사탕Icon from '@/assets/icons/사탕.png'
import 과자Icon from '@/assets/icons/과자.png'

const candies = ref([]);
const candyIcons = [젤리Icon, 초콜릿Icon, 사탕Icon, 과자Icon];

const createCandy = () => {
  const candy = {
    id: Math.random(),
    left: Math.random() * 90 + 5,
    rotation: Math.random() * 360,
    icon: candyIcons[Math.floor(Math.random() * candyIcons.length)]
  };
  
  candies.value.push(candy);
  
  setTimeout(() => {
    candies.value = candies.value.filter(c => c.id !== candy.id);
  }, 2000);
};

const spawnCandies = () => {
  for (let i = 0; i < 10; i++) {
    setTimeout(createCandy, i * 100);
  }
};

const getCandyStyle = (candy) => ({
  left: `${candy.left}%`,
  transform: `rotate(${candy.rotation}deg)`
});

onMounted(() => {
  spawnCandies();
});
</script>

<style scoped>
.candy-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1000;
}

.candy {
  position: absolute;
  top: -2rem;
}

.fall-enter-active {
  animation: fall 2s linear forwards;
}

@keyframes fall {
  0% {
    transform: translateY(0) rotate(0deg);
  }
  100% {
    transform: translateY(100vh) rotate(360deg);
  }
}
</style>