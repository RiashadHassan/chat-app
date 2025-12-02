import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from common.exceptions import RoomError

from .helpers import ChatConsumerHelper, MessageHandler

LOGGER = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = None
        self.room_name = None
        self.room_group_name = None

        self._helper = ChatConsumerHelper()
        self._messenger = MessageHandler()

    async def connect(self):
        try:
            # room is either a Channel or Thread instance
            self.room = await self._helper._get_room_from_db(self.scope)

            if not self.room:
                LOGGER.error("Room not found in DB. Closing connection.")
                await self.close()
                return

            self.room_name = self.room.uid
            self.room_group_name = f"chat_{self.room_name}"
        except RoomError as e:
            LOGGER.error("Closing the WS connection due to: %s", e)
            await self.close()
            return

        user = self.scope.get("user")
        if not user or user.is_anonymous:
            LOGGER.error("Unauthenticated user. Closing connection.")
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
        await self._messenger.save_message(self.room, message, self.scope.get("user"))
