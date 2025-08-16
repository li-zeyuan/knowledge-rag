from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ChatWithLLMSerializer, ChatDBWithHistorySerializer
from rest_framework import status
from llm.llm import format_prompt, get_answer
from llm.chat_qa_chain import chat_qa_whit_db_chain, chat_qa_whitout_db_chain
from .models import Chat, ChatTypeChatLLM
# Create your views here.

class ChatsView(viewsets.ViewSet):
    @action(methods=['post'], url_path='with_llm',detail=False)
    def with_llm(self, request):
        serializer = ChatWithLLMSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        prompt = serializer.validated_data.get("prompt", "")
        history = serializer.validated_data.get("history", [])
        llm = serializer.validated_data.get("llm", "")

        chat_item, isErr = self.response(prompt, history, llm)
        instance = Chat(prompt=prompt, bot_message=chat_item["bot_message"], chat_type=ChatTypeChatLLM, llm=llm, is_error=isErr)
        instance.save()

        return Response(chat_item)
    
    @action(methods=['post'], url_path='db_with_history',detail=False)
    def db_with_history(self, request):
        serializer = ChatDBWithHistorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        knowledge_db_name = serializer.validated_data.get("knowledge_db_name","")
        prompt = serializer.validated_data.get("prompt","")
        history = serializer.validated_data.get("history",[])
        llm = serializer.validated_data.get("llm","")

        chat_item = chat_qa_whit_db_chain(knowledge_db_name, prompt, llm,history)
        return Response(chat_item)
    
    @action( methods=['post'], url_path='db_without_history',detail=False)
    def db_without_history(self, request):
        serializer = ChatDBWithHistorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        knowledge_db_name = serializer.validated_data.get("knowledge_db_name","")
        prompt = serializer.validated_data.get("prompt","")
        llm = serializer.validated_data.get("llm","")

        chat_item = chat_qa_whitout_db_chain(knowledge_db_name, prompt, llm)
        return Response(chat_item)

    def response(self, prompt, history, llm, history_len = 3, temperature = 0.1, max_tokens = 2048):
        try:
            ctx_history = history[-history_len:]
            formatted_prompt = format_prompt(prompt, ctx_history)
            bot_message = get_answer(formatted_prompt, llm, temperature, max_tokens)

            return {"user_message": prompt, "bot_message": bot_message}, False
        except Exception as e:
            return {"user_message": prompt, "bot_message": e.user_message}, True