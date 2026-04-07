from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.app import App
from kivy.clock import Clock
import threading


class ProfileScreen(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)
        
        toolbar = MDTopAppBar(
            title="Profile",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
        )
        layout.add_widget(toolbar)
        
        layout.add_widget(MDBoxLayout(size_hint_y=0.1))
        
        self.username_label = MDLabel(
            text="Username: --",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=50,
        )
        layout.add_widget(self.username_label)
        
        self.email_label = MDLabel(
            text="Email: --",
            halign="center",
            size_hint_y=None,
            height=40,
        )
        layout.add_widget(self.email_label)
        
        self.stats_label = MDLabel(
            text="",
            halign="center",
            size_hint_y=None,
            height=80,
        )
        layout.add_widget(self.stats_label)
        
        layout.add_widget(MDBoxLayout(size_hint_y=0.3))
        
        logout_btn = MDRaisedButton(
            text="LOGOUT",
            size_hint_x=0.85,
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.8, 0.2, 0.2, 1),
            on_release=self.do_logout,
        )
        layout.add_widget(logout_btn)
        
        layout.add_widget(MDBoxLayout(size_hint_y=0.2))
        
        self.add_widget(layout)
    
    def on_enter(self):
        self.load_profile()
    
    def load_profile(self):
        threading.Thread(target=self._load_profile_thread, daemon=True).start()
    
    def _load_profile_thread(self):
        app = App.get_running_app()
        profile = app.api_service.get_profile()
        stats = app.api_service.get_usage_stats()
        Clock.schedule_once(lambda dt: self._display_profile(profile, stats))
    
    def _display_profile(self, profile, stats):
        data = profile.get('data', profile)
        self.username_label.text = f"Username: {data.get('username', '--')}"
        self.email_label.text = f"Email: {data.get('email', '--')}"
        
        stat_data = stats.get('data', stats)
        if isinstance(stat_data, dict):
            self.stats_label.text = (
                f"Total chats: {stat_data.get('total_sessions', 0)}\n"
                f"Total messages: {stat_data.get('total_messages', 0)}\n"
                f"Tokens used: {stat_data.get('total_tokens', 0)}"
            )
    
    def do_logout(self, *args):
        App.get_running_app().logout()
    
    def go_back(self):
        self.manager.current = 'chat_list'
