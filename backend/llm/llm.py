import openai
import zhipuai
import os
from langchain.chat_models  import ChatOpenAI
from .zhipuai_llm import ZhipuAILLM

def format_prompt(prompt, history):
    f_prompt = ""
    for turn in history:
        user_message, bot_message = turn
        f_prompt = f"{f_prompt}\nUser: {user_message}\nAssistant: {bot_message}"
    f_prompt = f"{f_prompt}\nUser: {prompt}\nAssistant: "

    return f_prompt

def get_answer(prompt, llm, temperature, max_tokens):
    if llm.startswith("gpt"):
        return answer_by_gpt(prompt, llm,temperature, max_tokens)
    elif llm.startswith("chatglm"):
        return get_completion_glm(prompt, llm,temperature, max_tokens)
    else:
        return "llm not supported"

def get_completion_glm(prompt, llm,temperature, max_tokens):
    zhipuai.api_key = os.getenv('ZHIPUAI_API_KEY', '')
    response = zhipuai.model_api.invoke(
        model=llm,
        prompt=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response["data"]["choices"][0]["content"].strip('"').strip(" ")

def answer_by_gpt(prompt, llm,temperature, max_tokens):
    messages = [{"role": "user", "content": prompt}]
    
    openai.api_key = os.getenv('OPENAI_API_KEY', '')
    response = openai.ChatCompletion.create(
        model=llm,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message["content"]

def model_to_llm(model, temperature:float = 0.0):
    if model.startswith("gpt"):
        return ChatOpenAI(model_name=model, temperature=temperature, openai_api_key=os.getenv('OPENAI_API_KEY', ''))
    if model.startswith("chatglm"):
        return ZhipuAILLM(model=model, temperature=temperature, zhipuai_api_key=os.getenv('ZHIPUAI_API_KEY', ''))
    else:
        raise ValueError(f"model{model} not support!!!")