from django.db import models


class AIModelConfig(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=200)
    max_tokens = models.IntegerField(default=2000)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'AI Model Configuration'
        verbose_name_plural = 'AI Model Configurations'

    def __str__(self):
        return self.display_name
