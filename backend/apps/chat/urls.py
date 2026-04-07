from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChatMessageListView, ChatSessionViewSet, SendMessageView

router = DefaultRouter()
router.register('sessions', ChatSessionViewSet, basename='chat-session')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'sessions/<uuid:session_id>/messages/',
        ChatMessageListView.as_view(),
        name='chat-messages',
    ),
    path(
        'sessions/<uuid:session_id>/send/',
        SendMessageView.as_view(),
        name='chat-send-message',
    ),
]
