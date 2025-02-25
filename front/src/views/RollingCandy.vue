<template>
  <div>
    <div class="title-wrapper">
      <div class="candy-container" ref="candyContainer"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// candy-container를 참조하기 위한 ref 생성
const candyContainer = ref(null);

// candy1.svg ~ candy10.svg 파일명 배열 생성
const candyImages = Array.from({ length: 10 }, (_, i) =>
    new URL(`../assets/candy/candy${i + 1}.svg`, import.meta.url).href
);
// 사탕 추가 함수
function addCandy(imageSrc, delay) {
    setTimeout(() => {
        if (candyContainer.value) {
            const candy = document.createElement('img');
            candy.src = imageSrc;
            candy.classList.add('candy'); // 먼저 클래스 추가
            candy.style.animation = 'none'; // 초기 애니메이션 해제
            candyContainer.value.appendChild(candy);

            // DOM 추가 후, 애니메이션 트리거
            setTimeout(() => {
                candy.style.animation = '';
            }, 50); // 애니메이션 트리거를 위한 약간의 지연시간
        }
    }, delay);
}

// 컴포넌트가 마운트된 후에 사탕 추가 로직 실행
onMounted(() => {
    candyImages.forEach((image, index) => {
        addCandy(image, index * 1000); // 1초 간격으로 추가
    });
});
</script>

<style scoped>
.title-wrapper {
  position: relative;
  text-align: center;
  /* 사탕 애니메이션을 위한 여유 공간 */
  margin-top: 10px; 
  width: 100%; /* 전체 너비 사용 */
}

h1 {
  font-size: 2.5rem;
  margin: 0;
  position: relative; /* 제목에 relative 추가 */
}

.candy-container {
  position: absolute;
  top: -20px; /* 제목과의 간격 조정 */
  left: 50%; /* 중앙 정렬의 기준점 */
  transform: translateX(-50%); /* 중앙 정렬 */
  width: 100%; /* 애니메이션을 위한 충분한 너비 */
  height: 40px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.candy {
  width: 40px;
  height: 40px;
  animation: roll-in 2s cubic-bezier(0.6, 0.05, 0.28, 0.91) forwards;
}

@keyframes roll-in {
  0% {
    transform: translateX(100vw) rotate(0deg);
  }
  80% {
    transform: translateX(5%) rotate(720deg);
  }
  100% {
    transform: translateX(0) rotate(720deg);
  }
}
</style>