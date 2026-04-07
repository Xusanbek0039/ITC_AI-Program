from rest_framework import serializers

from .models import AIModelConfig


class AIModelConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModelConfig
        fields = '__all__'
