import axios from "axios";

export function getLLMModels() {
  return axios.get("/api/models/llm_models/").then((res) => {
    if (res.status === 200) {
      return res.data;
    } else {
      return [];
    }
  });
}

export function getEmbeddingModels() {
  return axios.get("/api/models/embedding_models/").then((res) => {
    if (res.status === 200) {
      return res.data;
    } else {
      return [];
    }
  });
}

export function getChatHistory(data: any) {
  return axios.get("/api/chats/history", data).then((res) => {
    return res;
  });
}

export function chatWithLLM(data: any) {
  return axios.post("/api/chats/with_llm/", data).then((res) => {
    return res;
  });
}

export function chatKnowledgeWithHistory(data: any) {
  return axios.post("/api/chats/db_with_history/", data).then((res) => {
    return res;
  });
}

export function chatKnowledgeWithoutHistory(data: any) {
  return axios.post("/api/chats/db_without_history/", data).then((res) => {
    return res;
  });
}

export function clearChatHistory() {
  return axios.post("/api/chats/clear_history/").then((res) => {
    return res;
  });
}

export function getPresignedPutUrl(data: any) {
  return axios.post("/api/files/presigned_put/", data).then((res) => {
    return res;
  });
}

export function vectorizeFile(data: any) {
  return axios.post("/api/files/", data).then((res) => {
    return res;
  });
}

export function getKnowledgeDbNames() {
  return axios.get("/api/files/").then((res) => {
    return res;
  });
}
