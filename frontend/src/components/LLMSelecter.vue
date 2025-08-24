<script setup>
import { ref } from "vue";
import { NSelect } from "naive-ui";
import { getLLMModels, getEmbeddingModels } from "../api";

const LLMList = ref([]);
const LLMValue = ref("");
const embeddingModelList = ref([]);
const embeddingModelValue = ref("");

getLLMModels().then((res) => {
  for (const item of res) {
    LLMList.value.push({
      label: item,
      value: item,
      disabled: !item.includes("chatglm"),
    });
  }

  handleLLMValueChange(LLMList.value[0].value);
});

getEmbeddingModels().then((res) => {
  for (const item of res) {
    embeddingModelList.value.push({
      label: item,
      value: item,
      disabled: !item.includes("zhipuai"),
    });
  }

  handleEmbeddingModelValueChange(embeddingModelList.value[0].value);
});

// 定义要发送给父组件的事件
const emit = defineEmits(["update:llmValue", "update:embeddingValue"]);

function handleLLMValueChange(value) {
  LLMValue.value = value;
  // 向父组件发送更新事件
  emit("update:llmValue", value);
}

function handleEmbeddingModelValueChange(value) {
  embeddingModelValue.value = value;
  // 向父组件发送更新事件
  emit("update:embeddingValue", value);
}
</script>

<template>
  <div class="llm-selecter-container">
    <div>large language model</div>
    <n-select
      :value="LLMValue"
      :options="LLMList"
      @update:value="handleLLMValueChange"
    />

    <div>embedding model</div>
    <n-select
      :value="embeddingModelValue"
      :options="embeddingModelList"
      @update:value="handleEmbeddingModelValueChange"
    />
  </div>
</template>

<style scoped>
.llm-selecter-container {
  margin-top: 40px;
}
</style>