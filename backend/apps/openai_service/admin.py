from django.contrib import admin

from .models import AIModelConfig


@admin.register(AIModelConfig)
class AIModelConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'max_tokens', 'is_active', 'is_default', 'created_at')
    list_filter = ('is_active', 'is_default')
