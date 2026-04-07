from rest_framework import serializers

from .models import ChatMessage, ChatSession, UsageLog


class ChatSessionSerializer(serializers.ModelSerializer):
    message_count = serializers.SerializerMethodField()
    last_message_preview = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = [
            'id', 'title', 'is_active', 'model_name',
            'message_count', 'last_message_preview',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'message_count', 'last_message_preview',
            'created_at', 'updated_at',
        ]

    def get_message_count(self, obj):
        return obj.message_count

    def get_last_message_preview(self, obj):
        last = obj.last_message
        if last:
            return last.content[:100]
        return None


class ChatSessionDetailSerializer(ChatSessionSerializer):
    class Meta(ChatSessionSerializer.Meta):
        fields = ChatSessionSerializer.Meta.fields + ['system_prompt']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'session', 'role', 'content', 'tokens_used',
            'model_used', 'response_time', 'is_error', 'created_at',
        ]
        read_only_fields = [
            'id', 'role', 'tokens_used', 'model_used',
            'response_time', 'is_error', 'created_at',
        ]


class SendMessageSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be blank.")
        return value


class UsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageLog
        fields = '__all__'
        read_only_fields = [f.name for f in UsageLog._meta.get_fields() if hasattr(f, 'name')]
