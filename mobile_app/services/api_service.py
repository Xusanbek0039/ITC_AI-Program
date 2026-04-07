import requests
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class APIService:
    """HTTP client for communicating with Django backend API."""
    
    BASE_URL = "http://10.0.2.2:8000/api"  # Android emulator localhost
    TIMEOUT = 30
    
    def __init__(self):
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.session = requests.Session()
    
    def set_token(self, access_token: str, refresh_token: str = None):
        """Set authentication tokens."""
        self.access_token = access_token
        if refresh_token:
            self.refresh_token = refresh_token
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}'
        })
    
    def clear_token(self):
        """Clear authentication tokens."""
        self.access_token = None
        self.refresh_token = None
        self.session.headers.pop('Authorization', None)
    
    def _handle_response(self, response):
        """Process API response."""
        try:
            data = response.json()
        except ValueError:
            return {'success': False, 'message': 'Invalid server response'}
        
        if response.status_code == 401 and self.refresh_token:
            # Try to refresh token
            if self._refresh_access_token():
                return None  # Signal to retry
            
        if response.status_code >= 400:
            return {
                'success': False,
                'message': data.get('message', 'Request failed'),
                'errors': data.get('errors', {}),
                'status_code': response.status_code,
            }
        
        return data
    
    def _refresh_access_token(self) -> bool:
        """Attempt to refresh the access token."""
        try:
            response = requests.post(
                f"{self.BASE_URL}/auth/token/refresh/",
                json={'refresh': self.refresh_token},
                timeout=self.TIMEOUT,
            )
            if response.status_code == 200:
                data = response.json()
                self.set_token(data['access'], data.get('refresh', self.refresh_token))
                return True
        except Exception:
            pass
        return False
    
    def _request(self, method: str, endpoint: str, **kwargs):
        """Make an API request with error handling."""
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        kwargs.setdefault('timeout', self.TIMEOUT)
        
        try:
            response = self.session.request(method, url, **kwargs)
            result = self._handle_response(response)
            
            # Retry if token was refreshed
            if result is None:
                response = self.session.request(method, url, **kwargs)
                result = self._handle_response(response)
            
            return result
            
        except requests.ConnectionError:
            return {'success': False, 'message': 'Cannot connect to server. Check your internet connection.'}
        except requests.Timeout:
            return {'success': False, 'message': 'Request timed out. Please try again.'}
        except Exception as e:
            logger.error("API request error: %s", str(e))
            return {'success': False, 'message': 'An unexpected error occurred.'}
    
    # ===== Auth Endpoints =====
    
    def register(self, username: str, email: str, password: str, password_confirm: str):
        return self._request('POST', '/auth/register/', json={
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password_confirm,
        })
    
    def login(self, email: str, password: str):
        return self._request('POST', '/auth/login/', json={
            'email': email,
            'password': password,
        })
    
    def get_profile(self):
        return self._request('GET', '/auth/profile/')
    
    def update_profile(self, data: dict):
        return self._request('PATCH', '/auth/profile/', json=data)
    
    # ===== Chat Endpoints =====
    
    def create_chat(self, title: str = "New Chat"):
        return self._request('POST', '/chat/sessions/', json={'title': title})
    
    def list_chats(self, page: int = 1):
        return self._request('GET', f'/chat/sessions/?page={page}')
    
    def get_chat(self, session_id: str):
        return self._request('GET', f'/chat/sessions/{session_id}/')
    
    def delete_chat(self, session_id: str):
        return self._request('DELETE', f'/chat/sessions/{session_id}/')
    
    def rename_chat(self, session_id: str, title: str):
        return self._request('POST', f'/chat/sessions/{session_id}/rename/', json={'title': title})
    
    # ===== Message Endpoints =====
    
    def list_messages(self, session_id: str, page: int = 1):
        return self._request('GET', f'/chat/sessions/{session_id}/messages/?page={page}')
    
    def send_message(self, session_id: str, message: str):
        return self._request('POST', f'/chat/sessions/{session_id}/send/', json={'message': message})
    
    # ===== Usage =====
    
    def get_usage_stats(self):
        return self._request('GET', '/chat/sessions/usage_stats/')
