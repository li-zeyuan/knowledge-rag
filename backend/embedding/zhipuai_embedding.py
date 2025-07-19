from langchain.embeddings.base import Embeddings
from pydantic import BaseModel, root_validator
from typing import Optional, Dict, List
import os

class ZhipuAIEmbeddings(BaseModel, Embeddings):
    # key is string or None
    zhipuai_api_key: Optional[str] = None

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        values["zhipuai_api_key"] = os.getenv("ZHIPUAI_API_KEY", "")

        try:
            import zhipuai
            zhipuai.api_key = values["zhipuai_api_key"]
            values["client"] = zhipuai.model_api
        except ImportError:
            raise ValueError(
                "Zhipuai package not found, please install it with "
                "`pip install zhipuai`"
            )

        return values

    def _embed(self, texts: str) -> list[float]:
        try:
            resp = self.client.invoke(
                model="text_embedding",
                prompt=texts
            )
        except Exception as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")
        
        if resp["code"] != 200:
            raise ValueError(
                "Error raised by inference API HTTP code: %s, %s"
                % (resp["code"], resp["msg"])
            )
        
        return resp["data"]["embedding"]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(text) for text in texts]
    
    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError(
            "Please use `embed_documents`. Official does not support asynchronous requests")

    async def aembed_query(self, text: str) -> List[float]:
        raise NotImplementedError(
            "Please use `aembed_query`. Official does not support asynchronous requests")
        

  
