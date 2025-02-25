<template>
  <div class="chat-container">
    <div class="chat-area" ref="chatArea">
      <div v-for="(chat, index) in chatHistory" :key="index" :class="`${chat.type}-chat`">
        {{ chat.value }}
      </div>
    </div>
    <input
      type="text"
      v-model="chatInput"
      @keyup.enter="chatSubmit"
      class="chat-input"
      placeholder="Type your message..."
    />
  </div>
</template>

<script>
import { ref, nextTick } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const chatInput = ref('');
    const chatHistory = ref([]);
    const chatArea = ref(null);

    const OPEN_API_URL = 'https://api.openai.com/v1/chat/completions';
    const API_KEY = import.meta.env.VITE_CHATGPT_API_KEY;

    const headers = {
      Authorization: `Bearer ${API_KEY}`,
      'Content-Type': 'application/json',
    };

    const addChat = (type, value) => {
      const chat = { type, value };
      chatHistory.value.push(chat);
      nextTick(() => {
        chatArea.value.scrollTop = chatArea.value.scrollHeight;
      });
    };

    const chatReceive = (userMsg) => {
      const messages = [
        { role: 'user', content: userMsg },
      ];

      axios({
        method: 'post',
        url: OPEN_API_URL,
        headers,
        data: {
          model: 'gpt-3.5-turbo',
          messages,
        },
      })
        .then((res) => {
          const assistantMessage = res.data.choices[0].message.content;
          addChat('receive', assistantMessage);
        })
        .catch((err) => {
          console.log(err.response.data);
          console.log(err.response.status);
        });
    };

    const chatSubmit = () => {
      const userMsg = chatInput.value.trim();
      if (userMsg) {
        addChat('send', userMsg);
        chatReceive(userMsg);
        chatInput.value = '';
      }
    };

    return {
      chatInput,
      chatHistory,
      chatArea,
      chatSubmit,
    };
  },
};
</script>

<style scoped>
.chat-container {
  max-width: 500px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
  background: linear-gradient(to right, #a8edea, #fed6e3);
  border-radius: 20px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.chat-area {
  height: 400px;
  overflow-y: scroll;
  border: none;
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.05);
}

.chat-area::-webkit-scrollbar {
  width: 8px;
}

.chat-area::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 4px;
}

.chat-area::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #a8edea, #fed6e3);
  border-radius: 4px;
}

.chat-input {
  padding: 12px 20px;
  border: none;
  border-radius: 25px;
  background-color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.chat-input:focus {
  outline: none;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.send-chat {
  text-align: right;
  color: #2c3e50;
  font-weight: 600;
  margin: 10px 0;
  background-color: rgba(168, 237, 234, 0.3);
  padding: 10px 15px;
  border-radius: 15px 15px 0 15px;
  max-width: 80%;
  margin-left: auto;
  word-wrap: break-word;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.receive-chat {
  text-align: left;
  color: #2c3e50;
  background-color: rgba(254, 214, 227, 0.3);
  padding: 12px 18px;
  border-radius: 15px 15px 15px 0;
  margin: 10px 0;
  max-width: 80%;
  word-wrap: break-word;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  line-height: 1.6;
  font-size: 14px;
  white-space: pre-wrap;
}
</style>