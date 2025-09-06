from re import L
import re
import markdown
from plugins.chroma import get_vectordb
from .llm import model_to_llm
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.prompts import PromptTemplate

default_template_rq = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
    案。最多使用三句话。尽量使答案简明扼要。总是在回答的最后说“谢谢你的提问！”。
    {context}
    问题: {question}
    有用的回答:"""

def chat_qa_whit_db_chain(file, prompt,llm, history, top_k):
    vector_db = get_vectordb(file.id, file.embedding)
    if vector_db is None:
        return {"user_message": prompt, "bot_message": "vector_db is not found"}, True
    
    retriever = vector_db.as_retriever(search_type="similarity",  search_kwargs={'k': top_k})
    llm_model = model_to_llm(llm)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm= llm_model,
        retriever = retriever,
    )

    chat_history = []
    for turn in history:
        chat_history.append((turn["user_message"], turn["bot_message"]))

    result = qa_chain({"question": prompt, "chat_history": chat_history})
    answer = result["answer"]
    return {"user_message": prompt, "bot_message": answer}, False

def chat_qa_whitout_db_chain(file, prompt,llm, top_k, temperature):
    vector_db = get_vectordb(file.id, file.embedding)
    if vector_db is None:
        return {"user_message": prompt, "bot_message": "vector_db is not found"}, True
    
    retriever = vector_db.as_retriever(search_type="similarity",  search_kwargs={'k': top_k})
    llm_model = model_to_llm(llm)

    qa_prompt = PromptTemplate(input_variables=["context","question"],template=default_template_rq)
    qa_chain = RetrievalQA.from_chain_type(
        llm= llm_model,
        retriever = retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": qa_prompt}
    )

    result = qa_chain({"query": prompt,  "temperature": temperature, "top_k": top_k})
    answer = markdown_to_html(result["result"])
    return {"user_message": prompt, "bot_message": answer}, False

def markdown_to_html(markdown_text):
    if len(markdown_text) == 0:
        return ""

    html_text = markdown.markdown(markdown_text)
    # 替换\\n为<br>
    re_html_text = html_text.replace("\\n", "<br>")
    return re_html_text