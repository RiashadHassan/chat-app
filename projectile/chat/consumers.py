import json
import logging

from asgiref.sync import async_to_sync

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from typing import Dict, Any
from message.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        self._validate_room(self.scope)

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        user = self.scope.get("user")
        if not user or user.is_anonymous:
            await self.close()
            return
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data) if text_data else {}
        message = text_data_json.get("message", "No data was found.")
        context = {"type": "chat.message", "message": message}

        await self.channel_layer.group_send(self.room_group_name, context)

    async def chat_message(self, event):
        context = {"message": event.get("message")}
        await self.send(text_data=json.dumps(context))

    @database_sync_to_async
    def _validate_room(self, scope: Dict[str, Any]):
        chat_type = scope["url_route"]["kwargs"]["chat_type"]
        uid = scope["url_route"]["kwargs"]["uid"]
        print(chat_type, uid)

        pass
        # try:
