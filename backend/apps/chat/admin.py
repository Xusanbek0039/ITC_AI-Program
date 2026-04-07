from django.contrib import admin

from .models import ChatMessage, ChatSession, UsageLog


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'model_name', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'model_name', 'created_at']
    search_fields = ['title', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['role', 'short_content', 'session', 'tokens_used', 'is_error', 'created_at']
    list_filter = ['role', 'is_error', 'created_at']
    search_fields = ['content', 'session__title']
    readonly_fields = ['id', 'created_at']

    @admin.display(description='Content')
    def short_content(self, obj):
        return obj.content[:80]


@admin.register(UsageLog)
class UsageLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'model_used', 'total_tokens', 'cost_estimate', 'created_at']
    list_filter = ['model_used', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['id', 'created_at']
