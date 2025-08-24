<script setup>
import { ref, computed, nextTick, defineProps } from "vue";
import { NInput, NButton, NSelect, NAvatar } from "naive-ui";
import {
  chatWithLLM,
  getKnowledgeDbNames,
  getChatHistory,
  clearChatHistory,
} from "../api";

// 定义 props
const props = defineProps({
  selectedLlm: {
    type: String,
    default: "",
  },
  temperature: {
    type: Number,
    default: 0,
  },
  topK: {
    type: Number,
    default: 0,
  },
  historyLength: {
    type: Number,
    default: 0,
  },
});

const chatButLoading = ref(false);
const chatHistory = ref([]);

function fetchChatHistory() {
  getChatHistory()
    .then((res) => {
      chatHistory.value = res.data;
    })
    .finally(() => {
      // chatHistory渲染完成后滚动到history-container最底部
      scrollToBottom();
    });
}
fetchChatHistory();

const prompt = ref("");
const buttChatWithLLmDisabled = computed(() => {
  return prompt.value.length === 0;
});

function updatePrompt(value) {
  prompt.value = value;
}

function onChatWithLLM() {
  chatButLoading.value = true;
  chatWithLLM({
    prompt: prompt.value,
    llm: props.selectedLlm,
    temperature: props.temperature,
  })
    .then((res) => {
      prompt.value = "";
      fetchChatHistory();
    })
    .finally(() => {
      chatButLoading.value = false;
    });
}

const knowledgeDbName = ref("");
const knowledgeDbNames = ref([]);

getKnowledgeDbNames().then((res) => {
  for (const item of res.data.names) {
    knowledgeDbNames.value.push({
      label: item,
      value: item,
    });
  }

  if (knowledgeDbNames.value.length > 0) {
    knowledgeDbName.value = knowledgeDbNames.value[0].value;
  }
});

function updateKnowledgeDbName(value) {
  knowledgeDbName.value = value;
}

// 滚动到聊天历史底部
function scrollToBottom() {
  nextTick(() => {
    const historyContainer = document.querySelector(".history-container");
    if (historyContainer) {
      historyContainer.scrollTop = historyContainer.scrollHeight;
    }
  });
}
</script>

<template>
  <div class="chat-container">
    <div class="history-container">
      <div v-for="item in chatHistory" :key="item.id">
        <div class="user-message">
          <div class="user-message-content">{{ item.prompt }}</div>
          <n-avatar round size="medium" src="/src/assets/avatar.jpg" />
        </div>

        <div class="bot-message">
          <n-avatar round size="medium" src="/src/assets/pwa-192x192.png" />

          <div class="bot-message-content">{{ item.bot_message }}</div>
        </div>
      </div>
    </div>

    <div class="prompt-knowledge-container">
      <div class="prompt-container">
        <div>Prompt</div>
        <n-input
          :value="prompt"
          @update:value="updatePrompt"
          placeholder="Enter your prompt here"
          clearable
          @keydown.enter="onChatWithLLM"
        />
      </div>

      <div class="knowledge-container">
        <div>Select Knowledge</div>
        <n-select
          :value="knowledgeDbName"
          :options="knowledgeDbNames"
          @update:value="updateKnowledgeDbName"
        />
      </div>
    </div>

    <div class="button-container">
      <div class="button-chat">
        <n-button
          type="primary"
          :loading="chatButLoading"
          :disabled="buttChatWithLLmDisabled"
          @click="onChatWithLLM"
        >
          Chat with LLM
        </n-button>
        <n-button :loading="chatButLoading"
          >Chat knowledge with history</n-button
        >
        <n-button :loading="chatButLoading"
          >Chat knowledge without history</n-button
        >
      </div>

      <div class="button-clear">
        <n-button
          type="error"
          style="width: 100%"
          ghost
          @click="
            () => {
              clearChatHistory().then(() => {
                fetchChatHistory();
              });
            }
          "
          >Clear console</n-button
        >
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  width: 68%;
}

.history-container {
  width: 100%;
  height: 500px;
  /* 边框 */
  border: 1px solid #ccc;
  overflow-y: auto;
  padding-left: 10px;
  padding-right: 10px;
  padding-bottom: 20px;
}
.user-message {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
.bot-message {
  display: flex;
  justify-content: flex-start;
  margin-top: 20px;
}
.user-message-content,
.bot-message-content {
  max-width: 80%;
  margin-left: 10px;
  margin-right: 10px;
  padding-left: 5px;
  padding-right: 5px;
  display: flex;
  align-items: center;
  border-radius: 4px;
}
.user-message-content {
  background-color: #18a058;
}
.bot-message-content {
  color: #333639;
  background-color: #fafafc;
  /* margin-bottom: 20px; */
}

.prompt-knowledge-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 10px;
}
.prompt-container {
  width: 70%;
}
.knowledge-container {
  width: 28%;
}

.button-container {
  width: 100%;
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
.button-chat {
  width: 70%;
  display: flex;
  justify-content: space-between;
}
.button-clear {
  width: 28%;
}
</style>