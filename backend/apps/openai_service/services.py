import time
import logging
from typing import Optional

from openai import OpenAI, APIError, APITimeoutError, RateLimitError
from django.conf import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service layer for OpenAI API interactions."""

    DEFAULT_SYSTEM_PROMPT = (
        "You are a helpful AI assistant. You provide clear, accurate, "
        "and concise answers. If you don't know something, say so honestly."
    )

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.default_model = getattr(settings, 'OPENAI_DEFAULT_MODEL', 'gpt-4o-mini')
        self.max_tokens = getattr(settings, 'OPENAI_MAX_TOKENS', 2000)
        self.timeout = getattr(settings, 'OPENAI_TIMEOUT', 30)

    def get_response(self, session, user_message: str) -> dict:
        """
        Send message to OpenAI and get response.

        Args:
            session: ChatSession instance
            user_message: The user's message text

        Returns:
            dict with keys: content, model, prompt_tokens, completion_tokens,
                           total_tokens, response_time

        Raises:
            OpenAIServiceError on failure
        """
        messages = self._build_messages(session, user_message)
        model = session.model_name or self.default_model

        start_time = time.time()

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=self.max_tokens,
                timeout=self.timeout,
            )

            response_time = time.time() - start_time

            choice = response.choices[0]
            usage = response.usage

            return {
                'content': choice.message.content,
                'model': response.model,
                'prompt_tokens': usage.prompt_tokens,
                'completion_tokens': usage.completion_tokens,
                'total_tokens': usage.total_tokens,
                'response_time': round(response_time, 2),
            }

        except APITimeoutError:
            logger.error("OpenAI API timeout after %ss", self.timeout)
            raise OpenAIServiceError("AI service timed out. Please try again.")
        except RateLimitError:
            logger.error("OpenAI API rate limit exceeded")
            raise OpenAIServiceError("AI service is busy. Please wait and try again.")
        except APIError as e:
            logger.error("OpenAI API error: %s", str(e))
            raise OpenAIServiceError(f"AI service error: {str(e)}")
        except Exception as e:
            logger.error("Unexpected OpenAI error: %s", str(e))
            raise OpenAIServiceError("An unexpected error occurred.")

    def _build_messages(self, session, user_message: str) -> list:
        """Build the messages array for OpenAI API."""
        messages = []

        # System prompt
        system_prompt = session.system_prompt or self.DEFAULT_SYSTEM_PROMPT
        messages.append({"role": "system", "content": system_prompt})

        # Chat history (last 20 messages for context window management)
        history = session.messages.filter(
            is_error=False
        ).order_by('-created_at')[:20]

        for msg in reversed(list(history)):
            messages.append({
                "role": msg.role,
                "content": msg.content,
            })

        # Current user message
        messages.append({"role": "user", "content": user_message})

        return messages

    def estimate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Estimate cost based on model and token usage."""
        # Pricing per 1M tokens (approximate, update as needed)
        pricing = {
            'gpt-4o': {'input': 2.50, 'output': 10.00},
            'gpt-4o-mini': {'input': 0.15, 'output': 0.60},
            'gpt-3.5-turbo': {'input': 0.50, 'output': 1.50},
        }

        model_pricing = pricing.get(model, pricing['gpt-4o-mini'])

        input_cost = (prompt_tokens / 1_000_000) * model_pricing['input']
        output_cost = (completion_tokens / 1_000_000) * model_pricing['output']

        return round(input_cost + output_cost, 6)


class OpenAIServiceError(Exception):
    """Custom exception for OpenAI service errors."""
    pass
