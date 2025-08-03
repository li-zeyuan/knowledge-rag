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

export function chatWithLLm(data: any) {
  return axios.post("/api/chat/with_llm/", data).then((res) => {
    return res.data;
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
