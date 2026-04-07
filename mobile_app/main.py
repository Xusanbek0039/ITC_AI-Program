from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.chat_list_screen import ChatListScreen
from screens.chat_detail_screen import ChatDetailScreen
from screens.profile_screen import ProfileScreen
from services.api_service import APIService
from utils.storage import SecureStorage

# Set window size for testing
Window.size = (360, 640)


class AIChatApp(MDApp):
    """Main application class."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_service = APIService()
        self.storage = SecureStorage()
        self.current_user = None
    
    def build(self):
        self.title = "AI Chat"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.material_style = "M3"
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(ChatListScreen(name='chat_list'))
        sm.add_widget(ChatDetailScreen(name='chat_detail'))
        sm.add_widget(ProfileScreen(name='profile'))
        
        # Check saved token
        token = self.storage.get_token()
        if token:
            self.api_service.set_token(token)
            sm.current = 'chat_list'
        else:
            sm.current = 'login'
        
        return sm
    
    def logout(self):
        """Clear tokens and go to login."""
        self.storage.clear_token()
        self.api_service.clear_token()
        self.current_user = None
        self.root.current = 'login'


if __name__ == '__main__':
    AIChatApp().run()
