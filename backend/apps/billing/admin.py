from django.contrib import admin
from .models import SubscriptionPlan, UserQuota


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_monthly', 'max_messages_per_day', 'max_tokens_per_month', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(UserQuota)
class UserQuotaAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'messages_today', 'tokens_this_month', 'last_reset_date')
    list_filter = ('plan',)
    search_fields = ('user__email',)
