from rest_framework import serializers

from .models import ChatConversation, ChatMessage


class ChatbotRequestSerializer(serializers.Serializer):
    question = serializers.CharField()
    max_rows = serializers.IntegerField(min_value=1, default=50, required=False)
    conversation_id = serializers.IntegerField(required=False, allow_null=True)


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "question", "answer", "sql", "results", "created_at"]


class ChatConversationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatConversation
        fields = ["id", "title", "created_at", "updated_at"]


class ChatConversationDetailSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatConversation
        fields = ["id", "title", "created_at", "updated_at", "messages"]
