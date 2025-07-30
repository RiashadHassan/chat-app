class RoomHelper:
    VALID_CHAT_TYPES = ("channels", "threads", "gc", "dm")

    def __init__(self, room_name: str, *args, **kwargs):
        self.room_name = room_name

