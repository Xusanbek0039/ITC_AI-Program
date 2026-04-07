from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, TwoLineListItem, IconLeftWidget
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.clock import Clock
import threading


class ChatListScreen(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chats = []
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar(
            title="AI Chat",
            right_action_items=[
                ["account-circle", lambda x: self.go_to_profile()],
            ],
        )
        layout.add_widget(toolbar)
        
        # Chat list
        scroll = ScrollView()
        self.chat_list = MDList()
        scroll.add_widget(self.chat_list)
        layout.add_widget(scroll)
        
        # Empty state label
        self.empty_label = MDLabel(
            text="No chats yet.\nTap + to start a new chat!",
            halign="center",
            size_hint_y=None,
            height=100,
        )
        
        # FAB for new chat
        fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            on_release=self.create_new_chat,
        )
        
        self.add_widget(layout)
        self.add_widget(fab)
    
    def on_enter(self):
        """Load chats when screen is shown."""
        self.load_chats()
    
    def load_chats(self):
        threading.Thread(target=self._load_chats_thread, daemon=True).start()
    
    def _load_chats_thread(self):
        app = App.get_running_app()
        result = app.api_service.list_chats()
        Clock.schedule_once(lambda dt: self._display_chats(result))
    
    def _display_chats(self, result):
        self.chat_list.clear_widgets()
        
        if not result.get('success', True):
            if result.get('status_code') == 401:
                App.get_running_app().logout()
                return
            return
        
        chats = result.get('results', result.get('data', []))
        if isinstance(chats, dict):
            chats = chats.get('results', [])
        
        if not chats:
            self.chat_list.add_widget(self.empty_label)
            return
        
        for chat in chats:
            preview = chat.get('last_message_preview', 'No messages yet') or 'No messages yet'
            item = TwoLineListItem(
                text=chat.get('title', 'Untitled'),
                secondary_text=str(preview)[:80],
                on_release=lambda x, c=chat: self.open_chat(c),
            )
            self.chat_list.add_widget(item)
    
    def create_new_chat(self, *args):
        threading.Thread(target=self._create_chat_thread, daemon=True).start()
    
    def _create_chat_thread(self):
        app = App.get_running_app()
        result = app.api_service.create_chat()
        Clock.schedule_once(lambda dt: self._handle_new_chat(result))
    
    def _handle_new_chat(self, result):
        if result.get('success', True) and 'id' in result.get('data', result):
            chat = result.get('data', result)
            self.open_chat(chat)
    
    def open_chat(self, chat):
        app = App.get_running_app()
        detail_screen = self.manager.get_screen('chat_detail')
        detail_screen.session_id = chat.get('id', '')
        detail_screen.chat_title = chat.get('title', 'Chat')
        self.manager.current = 'chat_detail'
    
    def go_to_profile(self):
        self.manager.current = 'profile'
