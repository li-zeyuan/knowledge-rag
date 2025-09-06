<script setup>
import { ref, computed, nextTick, defineProps } from "vue";
import { NInput, NButton, NSelect, NAvatar } from "naive-ui";
import {
  chatWithLLM,
  chatKnowledgeWithHistory,
  chatKnowledgeWithoutHistory,
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

function onChatKnowledgeWithHistory() {
  chatButLoading.value = true;

  const history = [];
  for (const item of chatHistory.value.slice(-props.historyLength)) {
    history.push({
      user_message: item.prompt,
      bot_message: item.bot_message,
    });
  }

  chatKnowledgeWithHistory({
    knowledge_db_name: knowledgeDbName.value,
    prompt: prompt.value,
    history: history,
    llm: props.selectedLlm,
    top_k: props.topK,
  })
    .then((res) => {
      if (res.status === 200) {
        prompt.value = "";
        fetchChatHistory();
      }
    })
    .finally(() => {
      chatButLoading.value = false;
    });
}

function onChatKnowledgeWithoutHistory() {
  chatButLoading.value = true;
  chatKnowledgeWithoutHistory({
    knowledge_db_name: knowledgeDbName.value,
    prompt: prompt.value,
    llm: props.selectedLlm,
  })
    .then((res) => {
      if (res.status === 200) {
        prompt.value = "";
        fetchChatHistory();
      }
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

          <div class="bot-message-content" v-html="item.bot_message"></div>
          <!-- <div class="bot-message-content">{{ item.bot_message }}</div> -->
        </div>
      </div>
    </div>

    <div class="prompt-knowledge-container">
      <div class="prompt-container">
        <div>prompt</div>
        <n-input
          :value="prompt"
          @update:value="updatePrompt"
          placeholder="Enter your prompt here"
          clearable
          @keydown.enter="onChatWithLLM"
        />
      </div>

      <div class="knowledge-container">
        <div>select knowledge</div>
        <n-select
          :value="knowledgeDbName"
          :options="knowledgeDbNames"
          @update:value="updateKnowledgeDbName"
        />
      </div>
    </div>

    <div class="button-container">
      <div class="button-chat-container">
        <div class="button-chat-item">
          <n-button
            type="primary"
            :loading="chatButLoading"
            :disabled="buttChatWithLLmDisabled"
            @click="onChatWithLLM"
          >
            chat with llm
          </n-button>
        </div>

        <div class="button-chat-item">
          <n-button
            :loading="chatButLoading"
            :disabled="buttChatWithLLmDisabled"
            @click="onChatKnowledgeWithHistory"
            >chat knowledge with history</n-button
          >
        </div>

        <div class="button-chat-item">
          <n-button
            :loading="chatButLoading"
            :disabled="buttChatWithLLmDisabled"
            @click="onChatKnowledgeWithoutHistory"
            >chat knowledge without history</n-button
          >
        </div>
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
          >clear console</n-button
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
  white-space: pre-wrap;
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
.button-chat-container {
  width: 70%;
  display: flex;
  justify-content: space-between;
}

/* 第一个button-chat-item */
.button-chat-item:first-child {
  overflow: hidden;
  max-width: 24%;
}
/* 大于第一个button-chat-item */
.button-chat-item:nth-child(n + 2) {
  overflow: hidden;
  max-width: 38%;
}

.button-chat-item .n-button {
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.button-clear {
  width: 28%;
}
</style>