import logging

from channels.db import database_sync_to_async
from django.core.cache import cache
from typing import Dict, Any, Tuple

from common.exceptions import RoomError

from message.models import Message
from server.models import Channel, Thread

logger = logging.getLogger(__name__)


class ChatConsumerHelper:
    VALID_CHAT_TYPES: dict = {
        "channels": Channel,
        "threads": Thread,
        "gcs": Message,
        "dms": Message,
    }
    DEFAULT_CACHE_TIMEOUT: int = 60 * 60  # 1 hour

    def __init__(self, cache_timeout=None, *args, **kwargs):
        self.cache_timeout = cache_timeout or self.DEFAULT_CACHE_TIMEOUT

    async def validate_room(self, chat_type, uid):
        # ' ', ':' '/' doesn't work here
        room_name = f"{chat_type}-{uid}"
        validated_room_name = cache.get(room_name)

        if validated_room_name:
            logger.info("Fetched room from cache.")
            return validated_room_name

        if chat_type not in self.VALID_CHAT_TYPES:
            raise RoomError("Invalid chat_type.")

        channel = await self.db_validation(chat_type, uid)
        print("AAAAAAAAAAAAAAAAAAAAAAAa", channel)
        if not channel:
            raise RoomError("Room does not exist.")

        cache.set(room_name, True, self.cache_timeout)
        return room_name

    @database_sync_to_async
    def db_validation(self, chat_type, uid):
        db_model = self.VALID_CHAT_TYPES[chat_type]
        return db_model.objects.filter(uid=uid, is_deleted=False).first()

    async def _get_validated_room(self, scope: Dict[str, Any]) -> str:
        chat_type, uid = self._get_room_name(scope)
        validated_room_name = self.validate_room(chat_type, uid)
        return validated_room_name

    def _get_room_name(self, scope: Dict[str, Any]) -> Tuple[str, str]:
        chat_type = scope.get("url_route", {}).get("kwargs", {}).get("chat_type")
        uid = scope.get("url_route", {}).get("kwargs", {}).get("chat_uid")

        if not chat_type:
            raise RoomError("chat_type is missing.")
        if not uid:
            raise RoomError("chat_uid is missing.")

        return (chat_type, uid)
    
    @database_sync_to_async
    def _get_channel(self, scope: Dict[str, Any]) -> Channel:
        channel_uid = scope["url_route"]["kwargs"].get("chat_uid")
        try:
            return Channel.objects.get(uid=channel_uid)
        except Channel.DoesNotExist:
            return None
