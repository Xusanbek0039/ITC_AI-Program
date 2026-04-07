from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDTextButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.app import App
from kivy.clock import Clock
import threading


class RegisterScreen(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)
        
        toolbar = MDTopAppBar(
            title="Register",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
        )
        layout.add_widget(toolbar)
        
        layout.add_widget(MDBoxLayout(size_hint_y=0.1))
        
        title = MDLabel(
            text="Create Account",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=60,
        )
        layout.add_widget(title)
        
        self.username_field = MDTextField(
            hint_text="Username",
            mode="rectangle",
            size_hint_x=0.85,
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(self.username_field)
        
        self.email_field = MDTextField(
            hint_text="Email",
            mode="rectangle",
            size_hint_x=0.85,
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(self.email_field)
        
        self.password_field = MDTextField(
            hint_text="Password",
            mode="rectangle",
            password=True,
            size_hint_x=0.85,
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(self.password_field)
        
        self.password_confirm_field = MDTextField(
            hint_text="Confirm Password",
            mode="rectangle",
            password=True,
            size_hint_x=0.85,
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(self.password_confirm_field)
        
        self.error_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Error",
            size_hint_y=None,
            height=30,
        )
        layout.add_widget(self.error_label)
        
        register_btn = MDRaisedButton(
            text="REGISTER",
            size_hint_x=0.85,
            pos_hint={"center_x": 0.5},
            on_release=self.do_register,
        )
        layout.add_widget(register_btn)
        
        login_btn = MDTextButton(
            text="Already have an account? Login",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.go_back(),
        )
        layout.add_widget(login_btn)
        
        layout.add_widget(MDBoxLayout(size_hint_y=0.2))
        
        self.add_widget(layout)
    
    def do_register(self, *args):
        username = self.username_field.text.strip()
        email = self.email_field.text.strip()
        password = self.password_field.text.strip()
        password_confirm = self.password_confirm_field.text.strip()
        
        if not all([username, email, password, password_confirm]):
            self.error_label.text = "Please fill in all fields"
            return
        
        if password != password_confirm:
            self.error_label.text = "Passwords do not match"
            return
        
        if len(password) < 8:
            self.error_label.text = "Password must be at least 8 characters"
            return
        
        self.error_label.text = ""
        
        threading.Thread(
            target=self._register_thread,
            args=(username, email, password, password_confirm),
            daemon=True,
        ).start()
    
    def _register_thread(self, username, email, password, password_confirm):
        app = App.get_running_app()
        result = app.api_service.register(username, email, password, password_confirm)
        Clock.schedule_once(lambda dt: self._handle_register_result(result))
    
    def _handle_register_result(self, result):
        app = App.get_running_app()
        
        if result.get('success'):
            data = result.get('data', result)
            access = data.get('access') or data.get('access_token', '')
            refresh = data.get('refresh') or data.get('refresh_token', '')
            
            app.storage.save_token(access, refresh)
            app.api_service.set_token(access, refresh)
            self.manager.current = 'chat_list'
        else:
            self.error_label.text = result.get('message', 'Registration failed')
    
    def go_back(self):
        self.manager.current = 'login'
