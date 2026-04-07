from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ChatMessage, ChatSession

User = get_user_model()


class ChatTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(user=self.user)

        self.other_user = User.objects.create_user(
            email='otheruser@example.com',
            password='testpass123',
        )

    def test_create_session(self):
        response = self.client.post('/api/chat/sessions/', {
            'title': 'Test Session',
            'model_name': 'gpt-4o-mini',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Session')
        self.assertEqual(ChatSession.objects.filter(user=self.user).count(), 1)

    def test_list_sessions(self):
        ChatSession.objects.create(user=self.user, title='Session 1')
        ChatSession.objects.create(user=self.user, title='Session 2')
        ChatSession.objects.create(user=self.other_user, title='Other Session')

        response = self.client.get('/api/chat/sessions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    @patch('apps.chat.views.OpenAIService')
    def test_send_message(self, mock_openai_cls):
        mock_openai_cls.get_response.return_value = {
            'content': 'Hello! How can I help you?',
            'prompt_tokens': 10,
            'completion_tokens': 8,
            'total_tokens': 18,
            'model': 'gpt-4o-mini',
            'cost_estimate': 0.000027,
        }

        session = ChatSession.objects.create(user=self.user, title='New Chat')
        response = self.client.post(
            f'/api/chat/sessions/{session.id}/send/',
            {'message': 'Hello AI!'},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user_message', response.data)
        self.assertIn('assistant_message', response.data)
        self.assertEqual(response.data['user_message']['content'], 'Hello AI!')
        self.assertEqual(
            response.data['assistant_message']['content'],
            'Hello! How can I help you?',
        )

        # Verify title was auto-generated
        session.refresh_from_db()
        self.assertEqual(session.title, 'Hello AI!')

        # Verify messages were created
        self.assertEqual(ChatMessage.objects.filter(session=session).count(), 2)

    def test_list_messages(self):
        session = ChatSession.objects.create(user=self.user, title='Test')
        ChatMessage.objects.create(session=session, role='user', content='Hi')
        ChatMessage.objects.create(session=session, role='assistant', content='Hello!')

        response = self.client.get(f'/api/chat/sessions/{session.id}/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_delete_session(self):
        session = ChatSession.objects.create(user=self.user, title='To Delete')
        response = self.client.delete(f'/api/chat/sessions/{session.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ChatSession.objects.filter(id=session.id).count(), 0)

    def test_cannot_access_other_user_session(self):
        other_session = ChatSession.objects.create(
            user=self.other_user, title='Private',
        )

        # Cannot retrieve
        response = self.client.get(f'/api/chat/sessions/{other_session.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Cannot send message
        response = self.client.post(
            f'/api/chat/sessions/{other_session.id}/send/',
            {'message': 'Hack attempt'},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Cannot list messages
        response = self.client.get(
            f'/api/chat/sessions/{other_session.id}/messages/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
