from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ChatWithLLMSerializer, ChatDBSerializer
from rest_framework import status
from llm.llm import format_prompt, get_answer
from llm.chat_qa_chain import chat_qa_whit_db_chain, chat_qa_whitout_db_chain
from .models import Chat, ChatTypeChatLLM, ChatTypeChatKnowledgeWithHistory, ChatTypeChatKnowledgeWithoutHistory
from files.models import File
from llm.chat_qa_chain import markdown_to_html
# Create your views here.

class ChatsView(viewsets.ViewSet):
    @action(methods=['get'], url_path='history',detail=False)
    def history(self, request):
        chats = Chat.objects.all().order_by('id')

        data = []
        for c in chats:
            data.append(
                {
                    "id": c.id,
                    "prompt": c.prompt,
                    "bot_message": c.bot_message,
                    "is_error": c.is_error,
                    "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        return Response(data)

    @action(methods=['post'], url_path='with_llm',detail=False)
    def with_llm(self, request):
        serializer = ChatWithLLMSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        prompt = serializer.validated_data.get("prompt", "")
        llm = serializer.validated_data.get("llm", "")
        temperature = serializer.validated_data.get("temperature", 0.1)

        chat_item, isErr = self.response(prompt, llm, temperature)
        instance = Chat(prompt=prompt, bot_message=chat_item["bot_message"], chat_type=ChatTypeChatLLM, llm=llm, is_error=isErr)
        instance.save()

        return Response(chat_item)
    
    @action(methods=['post'], url_path='db_with_history',detail=False)
    def db_with_history(self, request):
        serializer = ChatDBSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        knowledge_db_name = serializer.validated_data.get("knowledge_db_name","")
        prompt = serializer.validated_data.get("prompt","")
        history = serializer.validated_data.get("history",[])
        llm = serializer.validated_data.get("llm","")
        top_k = serializer.validated_data.get("top_k", 3)

        file = File.objects.get(knowledge_db_name=knowledge_db_name)

        chat_item, isErr = chat_qa_whit_db_chain(file, prompt, llm, history, top_k)
        instance = Chat(prompt=prompt, bot_message=chat_item["bot_message"], chat_type=ChatTypeChatKnowledgeWithHistory, llm=llm, is_error=isErr)
        instance.save()
        return Response(chat_item)
    
    @action( methods=['post'], url_path='db_without_history',detail=False)
    def db_without_history(self, request):
        serializer = ChatDBSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        knowledge_db_name = serializer.validated_data.get("knowledge_db_name","")
        prompt = serializer.validated_data.get("prompt","")
        llm = serializer.validated_data.get("llm","")
        top_k = serializer.validated_data.get("top_k", 3)
        temperature = serializer.validated_data.get("temperature", 0.1)

        file = File.objects.get(knowledge_db_name=knowledge_db_name)

        chat_item, isErr = chat_qa_whitout_db_chain(file, prompt, llm, top_k, temperature)

        instance = Chat(prompt=prompt, bot_message=chat_item["bot_message"], chat_type=ChatTypeChatKnowledgeWithoutHistory, llm=llm, is_error=isErr)
        instance.save()
        return Response(chat_item)

    @action(methods=['post'], url_path='clear_history',detail=False)
    def clear_history(self, request):
        Chat.objects.all().delete()
        return Response(status=status.HTTP_200_OK)

    def response(self, prompt, llm, temperature = 0.1, max_tokens = 2048):
        try:
            formatted_prompt = format_prompt(prompt, [])
            bot_message = get_answer(formatted_prompt, llm, temperature, max_tokens)
            bot_message_html = markdown_to_html(bot_message)

            return {"user_message": prompt, "bot_message": bot_message_html}, False
        except Exception as e:
            return {"user_message": prompt, "bot_message": e.user_message}, True