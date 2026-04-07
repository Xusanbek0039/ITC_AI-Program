# TODO: Future models for billing and subscription management
from django.db import models
from django.conf import settings
import uuid


class SubscriptionPlan(models.Model):
    """Future: Subscription plans for users."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    max_messages_per_day = models.IntegerField(default=50)
    max_tokens_per_month = models.IntegerField(default=100000)
    allowed_models = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['price_monthly']

    def __str__(self):
        return f"{self.name} - ${self.price_monthly}/mo"


class UserQuota(models.Model):
    """Future: Track user usage quotas."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quota')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    messages_today = models.IntegerField(default=0)
    tokens_this_month = models.IntegerField(default=0)
    last_reset_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quota for {self.user.email}"
