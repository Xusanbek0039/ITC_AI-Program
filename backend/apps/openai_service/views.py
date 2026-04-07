from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import AIModelConfig
from .serializers import AIModelConfigSerializer


class ModelListView(generics.ListAPIView):
    serializer_class = AIModelConfigSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AIModelConfig.objects.filter(is_active=True)
