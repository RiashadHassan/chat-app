import logging
from typing import Dict, Any, Tuple, Union


from channels.db import database_sync_to_async

from django.core.cache import cache

from common.exceptions import RoomError

from message.models import Message
from server.models import Channel, Thread


LOGGER = logging.getLogger(__name__)


class ChatConsumerHelper:
    VALID_CHAT_TYPES: dict = {
        "channels": Channel,
        "threads": Thread,
        # "gcs": Message,
        # "dms": Message,
    }
    DEFAULT_CACHE_TIMEOUT: int = 60 * 60  # 1 hour

    def __init__(self, cache_timeout=None, *args, **kwargs):
        self.cache_timeout = cache_timeout or self.DEFAULT_CACHE_TIMEOUT

    async def _get_validated_room(self, scope: Dict[str, Any]) -> str:
        chat_type, uid = self._parse_chat_info(scope)
        return self.__validate_room(chat_type, uid)

    async def __validate_room(self, chat_type, uid):
        # ' ', ':' '/' doesn't work here
        room_name = f"{chat_type}-{uid}"
        validated_room_name = cache.get(room_name)

        if validated_room_name:
            LOGGER.info("Fetched room: %s from cache.", room_name)
            return validated_room_name

        if chat_type not in self.VALID_CHAT_TYPES:
            raise RoomError("Invalid chat_type.")

        cache.set(room_name, room_name, self.cache_timeout)
        return room_name

    def _parse_chat_info(self, scope: Dict[str, Any]) -> Tuple[str, str]:
        chat_type = scope.get("url_route", {}).get("kwargs", {}).get("chat_type")
        uid = scope.get("url_route", {}).get("kwargs", {}).get("chat_uid")

        if not chat_type:
            raise RoomError("chat_type is missing.")
        if not uid:
            raise RoomError("chat_uid is missing.")

        return (chat_type, uid)

    @database_sync_to_async
    def _get_room_from_db(self, scope: Dict[str, Any]) -> Union[Channel, Thread, None]:
        """
        Retrieve a Channel or Thread instance from the database based on
        chat_type and chat_uid found in the connection scope.
        This method is run in a synchronous context via database_sync_to_async.
        It does not raise RoomError; callers should decide how to handle None.
        """
        # extract chat_type and uid from the ASGI scope (will raise RoomError if missing)
        chat_type, uid = self._parse_chat_info(scope)

        # map chat_type to the corresponding DB model class (Channel or Thread for now)
        # TODO: add DM and Group chat features in the future
        db_model = self.VALID_CHAT_TYPES.get(chat_type)
        if not db_model:
            # unknown chat_type, nothing to query
            return None
        try:
            # only return active (not soft-deleted) room instances
            return db_model.objects.get(uid=uid, is_deleted=False)
        except db_model.DoesNotExist:
            # log the missing room and return None for the async caller to handle
            LOGGER.error("Room with uid %s does not exist.", uid)
            return None


class MessageHandler:
    async def save_message(
        self, room: Union[Channel, Thread], message: str, user
    ) -> Message:
        if isinstance(room, Channel):
            return await self.__save_channel_message(room, message, user)
        elif isinstance(room, Thread):
            return await self.__save_thread_message(room, message, user)
        else:
            raise RoomError("Unsupported room type for saving messages.")

    @database_sync_to_async
    def __save_channel_message(self, channel: Channel, message: str, user) -> Message:
        return Message.objects.create(channel=channel, content=message, author=user)

    @database_sync_to_async
    def __save_thread_message(self, thread: Thread, message: str, user) -> Message:
        return Message.objects.create(thread=thread, content=message, author=user)
