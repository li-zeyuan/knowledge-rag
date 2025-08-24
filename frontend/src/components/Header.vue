<script setup>
import { NAvatar } from "naive-ui";
</script>


<template>
  <header>
    <div class="logo">
      <a href="https://github.com/li-zeyuan/knowledge-rag">
        <NAvatar size="large" src="/src/assets/logo.svg"> </NAvatar>
      </a>
    </div>

    <div class="title">Knowledge RAG</div>
  </header>
</template>

<style scoped>
header {
  display: flex;
  align-items: center;
}

.logo {
  flex-basis: 33.33%;
}

.title {
  flex-basis: 33.33%;
  text-align: center;
  font-size: 40px;
  font-weight: bold;
}
</style>