<script setup>
import { NInputNumber, NSlider } from "naive-ui";
import { ref } from "vue";

const temperature = ref(0.01);
function handleTemperatureChange(value) {
  temperature.value = value;
}

const topK = ref(3);
function handleTopKChange(value) {
  topK.value = value;
}

const historyLength = ref(3);
function handleHistoryLengthChange(value) {
  historyLength.value = value;
}
</script>

<template>
  <div class="llm-setting-container">
    <h1>Parameter Setting</h1>
    <text>llm temperature</text>
    <n-input-number
      :min="0"
      :max="1"
      :step="0.01"
      :value="temperature"
      @update:value="handleTemperatureChange"
    ></n-input-number>
    <n-slider
      :min="0"
      :max="1"
      :step="0.01"
      :value="temperature"
      @update:value="handleTemperatureChange"
    ></n-slider>

    <text>top k</text>
    <n-input-number
      :min="0"
      :max="10"
      :step="1"
      :value="topK"
      @update:value="handleTopKChange"
    ></n-input-number>
    <n-slider
      :min="0"
      :max="10"
      :step="1"
      :value="topK"
      @update:value="handleTopKChange"
    ></n-slider>

    <text>history length</text>
    <n-input-number
      :min="0"
      :max="5"
      :step="1"
      :value="historyLength"
      @update:value="handleHistoryLengthChange"
    ></n-input-number>
    <n-slider
      :min="0"
      :max="5"
      :step="1"
      :value="historyLength"
      @update:value="handleHistoryLengthChange"
    ></n-slider>
  </div>
</template>

<style scoped>
</style>