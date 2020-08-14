import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message, Room
from django.contrib.auth import get_user_model


User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author = text_data_json['from']
        room_name = text_data_json['room']
        author_user = User.objects.filter(username=author)[0]
        room = Room.objects.filter(room=room_name)[0]
        m = Message(author=author_user, content=message, room=room)
        m.save()

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author_user': author
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        author = event['author_user']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'author': author
        }))