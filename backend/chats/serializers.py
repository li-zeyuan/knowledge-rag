from rest_framework import serializers

class ChatWithLLMSerializer(serializers.Serializer):
    history = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        ),
        required=False,
        allow_empty=True,
        help_text="对话历史，格式：[{'bot_message': 'xx', 'user_message': 'xx'}]"
    )
    prompt = serializers.CharField(
        required=True,
        help_text = "问题"
    )
    llm = serializers.CharField(
        required=True,
        help_text = "llm"
    )
    
   
class ChatDBWithHistorySerializer(serializers.Serializer):
    knowledge_db_name = serializers.CharField(
        required=True,
        help_text = "知识库名称"
    )
    history = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        ),
        required=False,
        allow_empty=True,
        help_text="对话历史，格式：[{'bot_message': 'xx', 'user_message': 'xx'}]"
    )
    prompt = serializers.CharField(
        required=True,
        help_text = "问题"
    )
    llm = serializers.CharField(
        required=True,
        help_text = "llm"
    )

class ChatDBWithoutHistorySerializer(serializers.Serializer):
    prompt = serializers.CharField(
        required=True,
        help_text = "问题"
    )
    llm = serializers.CharField(
        required=True,
        help_text = "llm"
    )