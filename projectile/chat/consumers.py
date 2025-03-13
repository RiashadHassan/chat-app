import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data) if text_data else {}
        message = text_data_json.get("message", "No Data Was Found")
        context = {"type": "chat.message", "message": message}

        async_to_sync(self.channel_layer.group_send)(self.room_group_name, context)

    def chat_message(self, event):
        context = {"message": event.get("message")}
        self.send(text_data=json.dumps(context))