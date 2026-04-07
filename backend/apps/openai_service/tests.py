from unittest.mock import MagicMock, patch, PropertyMock

from django.test import TestCase

from .services import OpenAIService, OpenAIServiceError


class MockMessage:
    def __init__(self, role, content):
        self.role = role
        self.content = content
        self.is_error = False
        self.created_at = None


class MockSession:
    def __init__(self, model_name=None, system_prompt=None, history=None):
        self.model_name = model_name
        self.system_prompt = system_prompt
        self._history = history or []
        self.messages = self._build_messages_manager()

    def _build_messages_manager(self):
        manager = MagicMock()
        qs = MagicMock()
        qs.order_by.return_value = list(reversed(self._history))
        manager.filter.return_value = qs
        return manager


class TestOpenAIServiceGetResponse(TestCase):
    @patch('apps.openai_service.services.OpenAI')
    @patch('apps.openai_service.services.settings')
    def test_get_response_success(self, mock_settings, mock_openai_cls):
        mock_settings.OPENAI_API_KEY = 'test-key'
        mock_settings.OPENAI_DEFAULT_MODEL = 'gpt-4o-mini'
        mock_settings.OPENAI_MAX_TOKENS = 2000
        mock_settings.OPENAI_TIMEOUT = 30

        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        mock_choice = MagicMock()
        mock_choice.message.content = "Hello! How can I help?"

        mock_usage = MagicMock()
        mock_usage.prompt_tokens = 10
        mock_usage.completion_tokens = 20
        mock_usage.total_tokens = 30

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_response.usage = mock_usage
        mock_response.model = 'gpt-4o-mini'

        mock_client.chat.completions.create.return_value = mock_response

        service = OpenAIService()
        session = MockSession(model_name='gpt-4o-mini')

        result = service.get_response(session, "Hi there")

        self.assertEqual(result['content'], "Hello! How can I help?")
        self.assertEqual(result['model'], 'gpt-4o-mini')
        self.assertEqual(result['prompt_tokens'], 10)
        self.assertEqual(result['completion_tokens'], 20)
        self.assertEqual(result['total_tokens'], 30)
        self.assertIn('response_time', result)

    @patch('apps.openai_service.services.OpenAI')
    @patch('apps.openai_service.services.settings')
    def test_get_response_timeout(self, mock_settings, mock_openai_cls):
        mock_settings.OPENAI_API_KEY = 'test-key'
        mock_settings.OPENAI_DEFAULT_MODEL = 'gpt-4o-mini'
        mock_settings.OPENAI_MAX_TOKENS = 2000
        mock_settings.OPENAI_TIMEOUT = 30

        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        from openai import APITimeoutError
        mock_client.chat.completions.create.side_effect = APITimeoutError(request=MagicMock())

        service = OpenAIService()
        session = MockSession(model_name='gpt-4o-mini')

        with self.assertRaises(OpenAIServiceError) as ctx:
            service.get_response(session, "Hi there")

        self.assertIn("timed out", str(ctx.exception))


class TestBuildMessages(TestCase):
    @patch('apps.openai_service.services.OpenAI')
    @patch('apps.openai_service.services.settings')
    def test_build_messages_with_history(self, mock_settings, mock_openai_cls):
        mock_settings.OPENAI_API_KEY = 'test-key'
        mock_settings.OPENAI_DEFAULT_MODEL = 'gpt-4o-mini'
        mock_settings.OPENAI_MAX_TOKENS = 2000
        mock_settings.OPENAI_TIMEOUT = 30

        mock_openai_cls.return_value = MagicMock()

        history = [
            MockMessage("user", "Hello"),
            MockMessage("assistant", "Hi! How can I help?"),
        ]

        session = MockSession(
            system_prompt="You are a test bot.",
            history=history,
        )

        # Make the queryset slicing work correctly
        qs_mock = MagicMock()
        qs_mock.order_by.return_value.__getitem__ = MagicMock(
            return_value=list(reversed(history))
        )
        session.messages.filter.return_value = qs_mock

        service = OpenAIService()
        messages = service._build_messages(session, "What is Python?")

        self.assertEqual(messages[0]['role'], 'system')
        self.assertEqual(messages[0]['content'], 'You are a test bot.')

        self.assertEqual(messages[-1]['role'], 'user')
        self.assertEqual(messages[-1]['content'], 'What is Python?')


class TestEstimateCost(TestCase):
    @patch('apps.openai_service.services.OpenAI')
    @patch('apps.openai_service.services.settings')
    def test_estimate_cost(self, mock_settings, mock_openai_cls):
        mock_settings.OPENAI_API_KEY = 'test-key'
        mock_settings.OPENAI_DEFAULT_MODEL = 'gpt-4o-mini'
        mock_settings.OPENAI_MAX_TOKENS = 2000
        mock_settings.OPENAI_TIMEOUT = 30

        mock_openai_cls.return_value = MagicMock()

        service = OpenAIService()

        # gpt-4o-mini: input $0.15/1M, output $0.60/1M
        cost = service.estimate_cost('gpt-4o-mini', 1000, 500)

        expected_input = (1000 / 1_000_000) * 0.15   # 0.00015
        expected_output = (500 / 1_000_000) * 0.60    # 0.0003
        expected = round(expected_input + expected_output, 6)

        self.assertEqual(cost, expected)

    @patch('apps.openai_service.services.OpenAI')
    @patch('apps.openai_service.services.settings')
    def test_estimate_cost_unknown_model_defaults(self, mock_settings, mock_openai_cls):
        mock_settings.OPENAI_API_KEY = 'test-key'
        mock_settings.OPENAI_DEFAULT_MODEL = 'gpt-4o-mini'
        mock_settings.OPENAI_MAX_TOKENS = 2000
        mock_settings.OPENAI_TIMEOUT = 30

        mock_openai_cls.return_value = MagicMock()

        service = OpenAIService()

        # Unknown model should fall back to gpt-4o-mini pricing
        cost = service.estimate_cost('unknown-model', 1000, 500)

        expected_input = (1000 / 1_000_000) * 0.15
        expected_output = (500 / 1_000_000) * 0.60
        expected = round(expected_input + expected_output, 6)

        self.assertEqual(cost, expected)
