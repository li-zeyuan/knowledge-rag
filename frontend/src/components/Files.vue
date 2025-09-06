<script setup>
import { ArchiveOutline as ArchiveIcon } from "@vicons/ionicons5";
import {
  NUpload,
  NUploadDragger,
  NIcon,
  NText,
  NP,
  NInput,
  NButton,
} from "naive-ui";
import { getPresignedPutUrl, vectorizeFile } from "../api";
import { ref, computed, defineProps } from "vue";
import axios from "axios";

const props = defineProps({
  selectedEmbedding: {
    type: String,
    default: "",
  },
});

const fileList = ref([]);
const fileNamePresignedKeyMap = ref({});

const knowledgeName = ref("");
function handleKnowledgeNameChange(value) {
  knowledgeName.value = value;
}

function handleFileListChange(value) {
  fileList.value = value;
}

const canVectorize = computed(() => {
  return knowledgeName.value.trim() !== "" && fileList.value.length > 0;
});

function clickVectorize() {
  const presignedKeys = [];
  for (const f of fileList.value) {
    const presignedKey = fileNamePresignedKeyMap.value[f.file.name];
    if (presignedKey) {
      presignedKeys.push(presignedKey);
    }
  }

  vectorizeFile({
    knowledge_db_name: knowledgeName.value,
    files: presignedKeys,
    embedding: props.selectedEmbedding,
  }).then((res) => {
    if (res.status === 200) {
      knowledgeName.value = "";
      fileList.value = [];
      fileNamePresignedKeyMap.value = {};
    }
  });
}

function uploadFile({ file, onFinish, onError, onProgress }) {
  getPresignedPutUrl({
    file_name: file.file.name,
  }).then((res) => {
    if (res.status === 200) {
      const presignedUrl = res.data.url;
      const presignedKey = res.data.key;
      fileNamePresignedKeyMap.value[file.file.name] = presignedKey;
      axios({
        method: "PUT",
        url: presignedUrl,
        data: file.file,
        onUploadProgress: (progressEvent) => {
          onProgress({
            percent: Math.round(
              (progressEvent.loaded * 100) / Number(progressEvent.total)
            ),
          });
        },
      })
        .then((res) => {
          onFinish();
        })
        .catch((err) => {
          console.error(err);
          onError();
        });
    }
  });
}
</script>
 
<template>
  <div class="files-container">
    <n-upload
      :custom-request="uploadFile"
      accept=".txt"
      :max="1"
      :file-list="fileList"
      @update:file-list="handleFileListChange"
    >
      <n-upload-dragger>
        <div style="margin-bottom: 12px">
          <n-icon size="48" :depth="3">
            <ArchiveIcon />
          </n-icon>
        </div>
        <n-text style="font-size: 16px"> Click or drag files here to upload. </n-text>
      </n-upload-dragger>
    </n-upload>

    <div class="vectorize-container">
      <div class="vectorize-input">
        <div>knowledge name</div>
        <n-input
          :value="knowledgeName"
          type="text"
          placeholder="Please enter the knowledge name"
          clearable
          @update:value="handleKnowledgeNameChange"
        />
      </div>

      <div class="vectorize-button">
        <n-button
          type="primary"
          :disabled="!canVectorize"
          @click="clickVectorize"
          >Vectorize</n-button
        >
      </div>
    </div>
  </div>
</template>

<style scoped>
.vectorize-container {
  display: flex;
  justify-content: space-between;
  margin-top: 6px;
}
.vectorize-input {
  width: 70%;
}
.vectorize-button {
  display: flex;
  align-items: flex-end;
}
</style>