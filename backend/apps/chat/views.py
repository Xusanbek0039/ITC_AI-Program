import logging
import time

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatMessage, ChatSession, UsageLog
from .serializers import (
    ChatMessageSerializer,
    ChatSessionDetailSerializer,
    ChatSessionSerializer,
    SendMessageSerializer,
    UsageLogSerializer,
)

logger = logging.getLogger(__name__)


class ChatSessionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ChatSessionSerializer
        return ChatSessionDetailSerializer

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def rename(self, request, pk=None):
        session = self.get_object()
        title = request.data.get('title', '').strip()
        if not title:
            return Response(
                {'error': 'Title is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        session.title = title
        session.save(update_fields=['title', 'updated_at'])
        serializer = self.get_serializer(session)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def usage_stats(self, request):
        user = request.user
        total_sessions = ChatSession.objects.filter(user=user).count()
        total_messages = ChatMessage.objects.filter(session__user=user).count()
        usage_agg = UsageLog.objects.filter(user=user).aggregate(
            total_tokens=Sum('total_tokens'),
        )
        return Response({
            'total_sessions': total_sessions,
            'total_messages': total_messages,
            'total_tokens': usage_agg['total_tokens'] or 0,
        })


class MessagePagination(PageNumberPagination):
    page_size = 50


class ChatMessageListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination

    def get_queryset(self):
        return ChatMessage.objects.filter(
            session__user=self.request.user,
            session_id=self.kwargs['session_id'],
        )


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        session = get_object_or_404(
            ChatSession, id=session_id, user=request.user,
        )

        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_text = serializer.validated_data['message']

        # Create user message
        user_message = ChatMessage.objects.create(
            session=session,
            role='user',
            content=user_text,
        )

        # Auto-generate title on first message
        if session.title == 'New Chat':
            session.title = user_text[:50]
            session.save(update_fields=['title', 'updated_at'])

        # Call OpenAI
        try:
            from apps.openai_service.services import OpenAIService

            start_time = time.time()
            ai_response = OpenAIService.get_response(session, user_text)
            response_time = time.time() - start_time

            assistant_message = ChatMessage.objects.create(
                session=session,
                role='assistant',
                content=ai_response.get('content', ''),
                tokens_used=ai_response.get('total_tokens', 0),
                model_used=ai_response.get('model', session.model_name),
                response_time=round(response_time, 3),
            )

            # Create usage log
            UsageLog.objects.create(
                user=request.user,
                session=session,
                prompt_tokens=ai_response.get('prompt_tokens', 0),
                completion_tokens=ai_response.get('completion_tokens', 0),
                total_tokens=ai_response.get('total_tokens', 0),
                model_used=ai_response.get('model', session.model_name),
                cost_estimate=ai_response.get('cost_estimate', 0),
            )

        except Exception as e:
            logger.error(f"OpenAI error for session {session_id}: {e}")
            assistant_message = ChatMessage.objects.create(
                session=session,
                role='assistant',
                content=f"Error: {str(e)}",
                is_error=True,
                model_used=session.model_name,
            )

        return Response(
            {
                'user_message': ChatMessageSerializer(user_message).data,
                'assistant_message': ChatMessageSerializer(assistant_message).data,
            },
            status=status.HTTP_201_CREATED,
        )
