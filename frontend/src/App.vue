<script setup>
import { ref } from "vue";
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";
import Chat from "./components/Chat.vue";
import Files from "./components/Files.vue";
import LLMSetting from "./components/LLMSetting.vue";
import LLMSelecter from "./components/LLMSelecter.vue";

// 接收来自 LLMSelecter 组件的值
const selectedLLM = ref("");
const selectedEmbedding = ref("");

// 处理 LLM 值更新
function handleLLMValueUpdate(value) {
  selectedLLM.value = value;
}
// 处理 Embedding 值更新
function handleEmbeddingValueUpdate(value) {
  selectedEmbedding.value = value;
}

const temperature = ref(0);
const topK = ref(0);
const historyLength = ref(0);
function handleTemperatureChange(value) {
  temperature.value = value;
}
function handleTopKChange(value) {
  topK.value = value;
}
function handleHistoryLengthChange(value) {
  historyLength.value = value;
}
</script>

<template>
  <div class="app">
    <Header />

    <div class="body">
      <Chat
        :selectedLlm="selectedLLM"
        :temperature="temperature"
        :topK="topK"
        :historyLength="historyLength"
      />
      <div class="right-container">
        <Files :selectedEmbedding="selectedEmbedding" />
        <LLMSelecter
          @update:llmValue="handleLLMValueUpdate"
          @update:embeddingValue="handleEmbeddingValueUpdate"
        />
        <LLMSetting
          @update:temperature="handleTemperatureChange"
          @update:topK="handleTopKChange"
          @update:historyLength="handleHistoryLengthChange"
        />
      </div>
    </div>

    <Footer />
  </div>
</template>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
}

.body {
  display: flex;
  justify-content: space-between;
}

.right-container {
  width: 30%;
}
</style>
