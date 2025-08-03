from langchain.document_loaders import UnstructuredFileLoader, tomarkdown
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from embedding.zhipuai_embedding import ZhipuAIEmbeddings
from plugins.minio import download_file
import os
import shutil

vector_db_dir = "backend/.vector_db"
knowledge_db_dir = "backend/.knowledge_db"

def create_db(id, fileKeys, embedding):
    if len(fileKeys) == 0:
        return "files is empty"

    loader = []
    for fileKey in fileKeys:
        local_file_path = f"{knowledge_db_dir}/{fileKey}"
        download_file(fileKey, local_file_path)
        loader.append(get_loader(local_file_path))

    docs  = []
    for l in loader:
        docs.extend(l.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
    split_docs = text_splitter.split_documents(docs)
    embedding_model = get_embedding(embedding)

    vector_db = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_model,
        persist_directory=f"{vector_db_dir}/{id}"
    )
    vector_db.persist()

    return
        
def get_loader(file_path):
    file_type = file_path.split(".")[-1]
    if file_type == "txt":
        return UnstructuredFileLoader(file_path)
    else:
        raise ValueError(f"file type :{file_type} not support")

def get_embedding(str):
    if str == "openai":
        return OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY', ''))
    elif str == "zhipuai":
        return ZhipuAIEmbeddings(zhipuai_api_key=os.getenv('ZHIPUAI_API_KEY', ''))
    else:
        raise ValueError(f"embedding type :{str} not support")

def get_knowledge_db_list():
    dirs = os.listdir(vector_db_dir)
    return dirs

def get_vectordb(knowledge_db_name):
    files = os.listdir(f"{vector_db_dir}/{knowledge_db_name}")
    if len(files) == 0:
        return None

    embedding = knowledge_db_name.split("|")[-1]
    embedding_model = get_embedding(embedding)

    vector_db = Chroma(
        persist_directory=f"{vector_db_dir}/{knowledge_db_name}",
        embedding_function=embedding_model
    )
    
    return vector_db

def delete_db(knowledge_db_name):
   shutil.rmtree(f"{vector_db_dir}/{knowledge_db_name}")