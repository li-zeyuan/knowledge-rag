<script setup>
import { NInputNumber, NSlider } from "naive-ui";
import { ref } from "vue";

const emit = defineEmits(["update:temperature", "update:topK", "update:historyLength"]);

const temperature = ref(0);
function handleTemperatureChange(value) {
  temperature.value = value;
  emit("update:temperature", value);
}
handleTemperatureChange(0.1);

const topK = ref(0);
function handleTopKChange(value) {
  topK.value = value;
  emit("update:topK", value);
}
handleTopKChange(3);

const historyLength = ref(0);
function handleHistoryLengthChange(value) {
  historyLength.value = value;
  emit("update:historyLength", value);
}
handleHistoryLengthChange(3);
</script>

<template>
  <div class="llm-setting-container">
    <div>llm temperature</div>
    <n-input-number
      :min="0"
      :max="1"
      :step="0.1"
      :value="temperature"
      @update:value="handleTemperatureChange"
    ></n-input-number>
    <n-slider
      :min="0"
      :max="1"
      :step="0.1"
      :value="temperature"
      @update:value="handleTemperatureChange"
    ></n-slider>

    <div>top k</div>
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

    <div>history length</div>
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
.llm-setting-container {
  margin-top: 40px;
}
</style>