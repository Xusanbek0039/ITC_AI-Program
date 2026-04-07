from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
import threading


class MessageBubble(MDCard):
    """Chat message bubble widget."""
    
    def __init__(self, text, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = dp(12)
        self.radius = [dp(12)]
        self.adaptive_height = True
        
        if is_user:
            self.md_bg_color = (0.2, 0.4, 0.8, 1)
            self.pos_hint = {"right": 0.98}
            self.size_hint_x = 0.75
        else:
            self.md_bg_color = (0.25, 0.25, 0.3, 1)
            self.pos_hint = {"x": 0.02}
            self.size_hint_x = 0.75
        
        label = MDLabel(
            text=text,
            adaptive_height=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
        )
        self.add_widget(label)


class ChatDetailScreen(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session_id = None
        self.chat_title = "Chat"
        self.is_loading = False
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        self.toolbar = MDTopAppBar(
            title="Chat",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
        )
        layout.add_widget(self.toolbar)
        
        # Messages area
        self.scroll = ScrollView(do_scroll_x=False)
        self.messages_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8),
            padding=[dp(8), dp(8), dp(8), dp(8)],
            size_hint_y=None,
            adaptive_height=True,
        )
        self.scroll.add_widget(self.messages_layout)
        layout.add_widget(self.scroll)
        
        # Loading indicator
        self.loading_label = MDLabel(
            text="AI is thinking...",
            halign="center",
            size_hint_y=None,
            height=dp(30),
            theme_text_color="Hint",
        )
        self.loading_label.opacity = 0
        layout.add_widget(self.loading_label)
        
        # Input area
        input_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            padding=[dp(8), dp(4), dp(4), dp(4)],
            spacing=dp(4),
        )
        
        self.message_input = MDTextField(
            hint_text="Type a message...",
            mode="rectangle",
            multiline=False,
            size_hint_x=0.85,
            on_text_validate=self.send_message,
        )
        input_layout.add_widget(self.message_input)
        
        send_btn = MDIconButton(
            icon="send",
            on_release=self.send_message,
        )
        input_layout.add_widget(send_btn)
        
        layout.add_widget(input_layout)
        self.add_widget(layout)
    
    def on_enter(self):
        self.toolbar.title = self.chat_title
        self.load_messages()
    
    def load_messages(self):
        if not self.session_id:
            return
        threading.Thread(target=self._load_messages_thread, daemon=True).start()
    
    def _load_messages_thread(self):
        app = App.get_running_app()
        result = app.api_service.list_messages(self.session_id)
        Clock.schedule_once(lambda dt: self._display_messages(result))
    
    def _display_messages(self, result):
        self.messages_layout.clear_widgets()
        
        messages = result.get('results', result.get('data', []))
        if isinstance(messages, dict):
            messages = messages.get('results', [])
        
        for msg in messages:
            is_user = msg.get('role') == 'user'
            bubble = MessageBubble(
                text=msg.get('content', ''),
                is_user=is_user,
            )
            self.messages_layout.add_widget(bubble)
        
        # Scroll to bottom
        Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)
    
    def _scroll_to_bottom(self):
        self.scroll.scroll_y = 0
    
    def send_message(self, *args):
        text = self.message_input.text.strip()
        if not text or self.is_loading:
            return
        
        self.message_input.text = ""
        self.is_loading = True
        self.loading_label.opacity = 1
        
        # Show user message immediately
        user_bubble = MessageBubble(text=text, is_user=True)
        self.messages_layout.add_widget(user_bubble)
        Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)
        
        threading.Thread(
            target=self._send_message_thread,
            args=(text,),
            daemon=True,
        ).start()
    
    def _send_message_thread(self, text):
        app = App.get_running_app()
        result = app.api_service.send_message(self.session_id, text)
        Clock.schedule_once(lambda dt: self._handle_ai_response(result))
    
    def _handle_ai_response(self, result):
        self.is_loading = False
        self.loading_label.opacity = 0
        
        if result.get('success', True):
            data = result.get('data', result)
            ai_msg = data.get('assistant_message', data.get('ai_message', {}))
            content = ai_msg.get('content', '') if isinstance(ai_msg, dict) else str(data.get('content', 'No response'))
            
            if content:
                ai_bubble = MessageBubble(text=content, is_user=False)
                self.messages_layout.add_widget(ai_bubble)
        else:
            error_bubble = MessageBubble(
                text=f"Error: {result.get('message', 'Failed to get response')}",
                is_user=False,
            )
            self.messages_layout.add_widget(error_bubble)
        
        Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)
    
    def go_back(self):
        self.messages_layout.clear_widgets()
        self.manager.current = 'chat_list'
