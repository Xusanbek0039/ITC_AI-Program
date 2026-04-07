# Message roles
ROLE_USER = 'user'
ROLE_ASSISTANT = 'assistant'
ROLE_SYSTEM = 'system'

ROLE_CHOICES = [
    (ROLE_USER, 'User'),
    (ROLE_ASSISTANT, 'Assistant'),
    (ROLE_SYSTEM, 'System'),
]

# Default values
DEFAULT_CHAT_TITLE = 'New Chat'
DEFAULT_MODEL = 'gpt-4o-mini'
MAX_MESSAGE_LENGTH = 10000
MAX_CHAT_TITLE_LENGTH = 255

# Rate limit
DEFAULT_RATE_LIMIT_USER = '60/min'
DEFAULT_RATE_LIMIT_ANON = '10/min'
