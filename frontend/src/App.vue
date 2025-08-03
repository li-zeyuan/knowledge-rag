<script setup>
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";
import Chat from "./components/Chat.vue";
import Files from "./components/Files.vue";
import LLMSetting from "./components/LLMSetting.vue";
import LLMSelecter from "./components/LLMSelecter.vue";
</script>

<template>
  <div class="app">
    <Header />

    <div class="main">
      <Chat />
      <Files />
      <LLMSetting />
      <LLMSelecter />
    </div>

    <Footer />
  </div>
</template>

<style scoped>
</style>
