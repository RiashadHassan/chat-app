import json
import logging

from asgiref.sync import sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async

from common.exceptions import RoomError

from .helpers import ChatConsumerHelper
from server.models import Channel
from message.models import Message

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = None
        self.room_name = None
        self.room_group_name = None

        self._helper = ChatConsumerHelper()

    async def connect(self):
        try:
            self.channel = await self._helper._get_channel(self.scope)
            if not self.channel:
                logger.error("Channel not found. Closing connection.")
                await self.close()
                return

            self.room_name = self.channel.uid
            self.room_group_name = f"chat_{self.room_name}"
        except RoomError as e:
            logger.error("Closing the WS connection due to: %s", e)
            await self.close()
            return

        user = self.scope.get("user")
        if not user or user.is_anonymous:
            logger.error("Unauthenticated user. Closing connection.")
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data or "{}")
        except json.JSONDecodeError:
            text_data_json = {}

        message = text_data_json.get("message", "No data was found.")
        context = {"type": "chat.message", "message": message}

        await self.channel_layer.group_send(self.room_group_name, context)

    async def chat_message(self, event):
        message = event.get("message")
        context = {"message": message}
        await self.send(text_data=json.dumps(context))
        await self.__save_message(message)

    @database_sync_to_async
    def __save_message(self, message):
        Message.objects.create(
            channel=self.channel,
            content=message,
            author=self.scope.get("user"),
        )
