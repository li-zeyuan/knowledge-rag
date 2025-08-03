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
    });
  }

  LLMValue.value = LLMList.value[0].value;
});

getEmbeddingModels().then((res) => {
  for (const item of res) {
    embeddingModelList.value.push({
      label: item,
      value: item,
    });
  }

  embeddingModelValue.value = embeddingModelList.value[0].value;
});

function handleLLMValueChange(value) {
  LLMValue.value = value;
}

function handleEmbeddingModelValueChange(value) {
  embeddingModelValue.value = value;
}
</script>

<template>
  <div class="llm-selecter-container">
    <h1>large language model</h1>
    <n-select
      :value="LLMValue"
      :options="LLMList"
      @update:value="handleLLMValueChange"
    />

    <h1>embedding model</h1>
    <n-select
      :value="embeddingModelValue"
      :options="embeddingModelList"
      @update:value="handleEmbeddingModelValueChange"
    />
  </div>
</template>

<style scoped>
</style>