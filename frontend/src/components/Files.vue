<script setup>
import { ArchiveOutline as ArchiveIcon } from "@vicons/ionicons5";
import { NUpload, NUploadDragger, NIcon, NText, NP } from "naive-ui";

const handleFinish = (data) => {
  debugger;
  console.log(data);
};
</script>


<template>
  <div class="files-container">
    <n-upload accept=".txt,.png" max="1" @change="handleFinish">
      <n-upload-dragger>
        <div style="margin-bottom: 12px">
          <n-icon size="48" :depth="3">
            <ArchiveIcon />
          </n-icon>
        </div>
        <n-text style="font-size: 16px"> 点击或拖动文件到此区域上传 </n-text>
      </n-upload-dragger>
    </n-upload>
  </div>
</template>

<style scoped>
</style>