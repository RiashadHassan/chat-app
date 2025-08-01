import json
import logging

from asgiref.sync import sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async

from common.exceptions import RoomError

from .helpers import ChatConsumerHelper
from server.models import Channel

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._helper = ChatConsumerHelper()

    async def connect(self):
        channel = await self.get_channel()
        print(channel)
        try:

            self.room_name = await self._helper._get_validated_room(self.scope)
            self.room_group_name = f"chat_{self.room_name}"
            print("2222222222222222222222222", self.room_group_name)
        except RoomError as e:
            logger.error("Closing the WS connection due to: %s", e)
            await self.close()
            return

        user = self.scope.get("user")
        if not user or user.is_anonymous:
            await self.close()
            return


        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
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
    def get_channel(self):
        return Channel.objects.all().first()
