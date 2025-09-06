from rest_framework import serializers

class ChatWithLLMSerializer(serializers.Serializer):
    prompt = serializers.CharField(
        required=True,
        help_text = "问题"
    )
    llm = serializers.CharField(
        required=True,
        help_text = "llm"
    )
    temperature = serializers.FloatField(
        required=True,
        help_text = "温度"
    )
   
class ChatDBSerializer(serializers.Serializer):
    knowledge_db_name = serializers.CharField(
        required=True,
        help_text = "知识库名称"
    )
    history = serializers.ListField(
        child=serializers.DictField(
            allow_empty=False,
            child=serializers.CharField(allow_blank=True)
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
    top_k = serializers.IntegerField(
        required=False,
        default=3,
        help_text="检索结果数量"
    )
    temperature = serializers.FloatField(
        required=False,
        default=0.1,
        help_text="温度"
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