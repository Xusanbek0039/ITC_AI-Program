from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDTextButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.app import App
from kivy.clock import Clock
import threading


class LoginScreen(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Top bar
        toolbar = MDTopAppBar(title="AI Chat - Login")
        layout.add_widget(toolbar)
        
        # Spacer
        layout.add_widget(MDBoxLayout(size_hint_y=0.2))
        
        # Title
        title = MDLabel(
            text="Welcome Back",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=60,
        )
        layout.add_widget(title)
        
        # Email field
        self.email_field = MDTextField(
            hint_text="Email",
            mode="rectangle",
            size_hint_x=0.85,
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(self.email_field)
        
        # Password field
        self.password_field = MDTextField(
            hint_text="Password",
            mode="rectangle",
            password=True,
            size_hint_x=0.85,
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(self.password_field)
        
        # Error label
        self.error_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Error",
            size_hint_y=None,
            height=30,
        )
        layout.add_widget(self.error_label)
        
        # Login button
        login_btn = MDRaisedButton(
            text="LOGIN",
            size_hint_x=0.85,
            pos_hint={"center_x": 0.5},
            on_release=self.do_login,
        )
        layout.add_widget(login_btn)
        
        # Register link
        register_btn = MDTextButton(
            text="Don't have an account? Register",
            pos_hint={"center_x": 0.5},
            on_release=self.go_to_register,
        )
        layout.add_widget(register_btn)
        
        # Spacer
        layout.add_widget(MDBoxLayout(size_hint_y=0.3))
        
        self.add_widget(layout)
    
    def do_login(self, *args):
        email = self.email_field.text.strip()
        password = self.password_field.text.strip()
        
        if not email or not password:
            self.error_label.text = "Please fill in all fields"
            return
        
        self.error_label.text = ""
        
        # Run API call in background thread
        threading.Thread(
            target=self._login_thread,
            args=(email, password),
            daemon=True,
        ).start()
    
    def _login_thread(self, email, password):
        app = App.get_running_app()
        result = app.api_service.login(email, password)
        Clock.schedule_once(lambda dt: self._handle_login_result(result))
    
    def _handle_login_result(self, result):
        app = App.get_running_app()
        
        if result.get('success'):
            data = result.get('data', result)
            access = data.get('access') or data.get('access_token', '')
            refresh = data.get('refresh') or data.get('refresh_token', '')
            
            app.storage.save_token(access, refresh)
            app.api_service.set_token(access, refresh)
            self.manager.current = 'chat_list'
        else:
            self.error_label.text = result.get('message', 'Login failed')
    
    def go_to_register(self, *args):
        self.manager.current = 'register'
