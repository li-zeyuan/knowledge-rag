<script setup>
import { ref, computed } from "vue";
import { NInput, NButton, NSelect } from "naive-ui";
import { chatWithLLM, getKnowledgeDbNames } from "../api";

const prompt = ref("");
const buttChatWithLLmDisabled = computed(() => {
  return prompt.value.length === 0;
});

function updatePrompt(value) {
  prompt.value = value;
}

function onChatWithLLM() {
  chatWithLLM({
    prompt: prompt.value,
    llm: "chatglm", // todo
    history: [], // todo
  }).then((res) => {
    console.log(res);
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
</script>

<template>
  <div>
    <div class="chat-container">
      <h1>Chat</h1>
    </div>
    <div class="prompt-container">
      <n-input
        :value="prompt"
        @update:value="updatePrompt"
        placeholder="Enter your prompt here"
        clearable="true"
      />
    </div>
    <div class="button-container">
      <n-button :disabled="buttChatWithLLmDisabled" @click="onChatWithLLM">
        Chat with LLM
      </n-button>
      <n-button>Chat history</n-button>
      <n-button>Chat knowledge with history</n-button>
      <n-button>Chat knowledge without history</n-button>
      <n-select
        :value="knowledgeDbName"
        :options="knowledgeDbNames"
        @update:value="updateKnowledgeDbName"
      />
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  height: 400px;
  /* 边框 */
  border: 1px solid #ccc;
}
</style>