import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"

#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )

#         self.accept()

#     def disconnect(self, code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     def receive(self, text_data=None, bytes_data=None):
#         text_data_json = json.loads(text_data) if text_data else {}
#         message = text_data_json.get("message", "No Data Was Found")
#         context = {"type": "chat.message", "message": message}

#         async_to_sync(self.channel_layer.group_send)(self.room_group_name, context)

#     def chat_message(self, event):
#         context = {"message": event.get("message")}
#         from message.models import Message
#         Message.objects.create(content = context)
#         self.send(text_data=json.dumps(context))

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        
    DEFAULT_ROOM_NAME = "Wrong_URL"
    async def connect(self):
        try:
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        except RoomNameError as e:
            self.logger.error(f"Error getting room name: {str(e)}")
            self.room_name = self.DEFAULT_ROOM_NAME
            #TODO: send a general "Wrong URL message to everyone who encounters this error"
            
        self.room_group_name = f"chat_{self.room_name}"

        self.channel_layer.group_add(self.room_group_name, self.channel_name)
        
        self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data) if text_data else {}
        message = text_data_json.get("message", "No data was found.")
        context = {"type": "chat.message", "message":message}
        
        self.channel_layer.group_send(self.room_group_name, context)

    async def chat_message(self, event):
        context = {"message": event.get("message")}
        self.send(text_data=json.dumps(context))

class RoomNameError(Exception):
    pass