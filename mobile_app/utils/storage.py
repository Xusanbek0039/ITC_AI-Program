from kivy.storage.jsonstore import JsonStore
import os


class SecureStorage:
    """Local storage for tokens and user preferences."""
    
    def __init__(self):
        store_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(store_path, exist_ok=True)
        self.store = JsonStore(os.path.join(store_path, 'app_data.json'))
    
    def save_token(self, access_token: str, refresh_token: str):
        self.store.put('auth', access_token=access_token, refresh_token=refresh_token)
    
    def get_token(self):
        if self.store.exists('auth'):
            data = self.store.get('auth')
            return data.get('access_token')
        return None
    
    def get_refresh_token(self):
        if self.store.exists('auth'):
            data = self.store.get('auth')
            return data.get('refresh_token')
        return None
    
    def clear_token(self):
        if self.store.exists('auth'):
            self.store.delete('auth')
    
    def save_setting(self, key: str, value):
        self.store.put(f'setting_{key}', value=value)
    
    def get_setting(self, key: str, default=None):
        store_key = f'setting_{key}'
        if self.store.exists(store_key):
            return self.store.get(store_key).get('value', default)
        return default
