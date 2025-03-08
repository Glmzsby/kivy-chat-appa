from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
import socket
import threading
import json
from kivy.utils import platform

# 客户端配置
SERVER_HOST = '127.0.0.1'  # 替换为服务器的实际 IP 地址
SERVER_PORT = 5555
BUFFER_SIZE = 1024

class ChatClientApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client_socket = None
        self.username = ""
        self.target_user = ""
        self.messages = []

    def build(self):
        # 主布局
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # 标题
        self.title_label = Label(
            text="Mobile Chat Client", 
            font_size=24, 
            size_hint_y=None, 
            height=50
        )
        self.layout.add_widget(self.title_label)

        # 登录界面
        self.login_layout = BoxLayout(
            orientation='vertical', 
            spacing=10, 
            size_hint_y=None, 
            height=200
        )
        self.username_input = TextInput(
            hint_text="Enter username", 
            multiline=False,
            size_hint_y=None,
            height=40
        )
        self.password_input = TextInput(
            hint_text="Enter password", 
            multiline=False, 
            password=True,
            size_hint_y=None,
            height=40
        )
        self.login_button = Button(
            text="Login",
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.6, 1, 1),
            on_press=self.login
        )
        self.login_layout.add_widget(self.username_input)
        self.login_layout.add_widget(self.password_input)
        self.login_layout.add_widget(self.login_button)
        self.layout.add_widget(self.login_layout)

        # 聊天界面（初始隐藏）
        self.chat_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # 用户列表
        self.user_list = GridLayout(cols=1, size_hint_y=None)
        self.user_list.bind(minimum_height=self.user_list.setter('height'))
        self.user_scroll = ScrollView(size_hint=(1, 0.3))
        self.user_scroll.add_widget(self.user_list)
        
        # 聊天历史
        chat_history_scroll = ScrollView(size_hint=(1, 1))
        self.chat_history = Label(
            text="",
            size_hint_y=None,
            height=300,
            valign='top',
            halign='left',
            text_size=(None, None)
        )
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        chat_history_scroll.add_widget(self.chat_history)

        # 消息输入区域
        input_area = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50
        )
        self.message_input = TextInput(
            hint_text="Type a message...",
            multiline=False,
            size_hint=(0.8, 1)
        )
        self.send_button = Button(
            text="Send",
            size_hint=(0.2, 1),
            background_color=(0.2, 0.6, 1, 1),
            on_press=self.send_message
        )
        input_area.add_widget(self.message_input)
        input_area.add_widget(self.send_button)

        self.chat_layout.add_widget(self.user_scroll)
        self.chat_layout.add_widget(chat_history_scroll)
        self.chat_layout.add_widget(input_area)
        
        self.chat_layout.opacity = 0  # 初始隐藏
        self.layout.add_widget(self.chat_layout)

        # Android特定的权限请求
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.INTERNET])

        return self.layout

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not password:
            self.show_error("Please enter both username and password.")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))

            # 发送登录请求
            self.client_socket.send(json.dumps({
                'type': 'login',
                'username': username,
                'password': password
            }).encode())

            response = self.client_socket.recv(BUFFER_SIZE).decode()
            if json.loads(response)['status'] == 'success':
                self.username = username
                self.login_layout.opacity = 0
                self.chat_layout.opacity = 1
                self.start_receive_thread()
                self.request_user_list()
            else:
                self.show_error("Invalid credentials.")
        except Exception as e:
            self.show_error(f"Connection failed: {str(e)}")

    def start_receive_thread(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(BUFFER_SIZE)
                if data:
                    message = json.loads(data.decode('utf-8'))
                    if message['type'] == 'message':
                        self.messages.append(message)
                        Clock.schedule_once(lambda dt: self.update_chat_history())
                    elif message['type'] == 'user_list':
                        Clock.schedule_once(lambda dt: self.update_user_list(message['users']))
            except Exception as e:
                print(f"Error receiving messages: {e}")
                break

    def request_user_list(self):
        self.client_socket.send(json.dumps({'type': 'get_users'}).encode())

    def update_user_list(self, users):
        self.user_list.clear_widgets()
        for user in users:
            if user != self.username:
                btn = Button(
                    text=user,
                    size_hint_y=None,
                    height=50,
                    background_color=(0.9, 0.9, 0.9, 1),
                    on_press=self.select_user
                )
                self.user_list.add_widget(btn)

    def select_user(self, instance):
        self.target_user = instance.text
        self.update_chat_history()

    def update_chat_history(self):
        self.chat_history.text = ""
        for msg in self.messages:
            if (msg['sender'] == self.username and msg['receiver'] == self.target_user) or \
               (msg['sender'] == self.target_user and msg['receiver'] == self.username):
                prefix = "You: " if msg['sender'] == self.username else f"{msg['sender']}: "
                self.chat_history.text += f"[{msg['timestamp']}] {prefix}{msg['content']}\n"

    def send_message(self, instance):
        message = self.message_input.text.strip()
        if message and self.target_user:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg_obj = {
                'type': 'message',
                'sender': self.username,
                'receiver': self.target_user,
                'content': message,
                'timestamp': timestamp
            }
            self.client_socket.send(json.dumps(msg_obj).encode())
            self.messages.append(msg_obj)
            self.update_chat_history()
            self.message_input.text = ""

    def show_error(self, message):
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()

if __name__ == "__main__":
    from kivy.core.window import Window
    if platform != 'android':
        Window.size = (360, 640)  # 仅在非Android平台设置窗口大小
    ChatClientApp().run()
