from django.db import models
from base.models import BaseModelWithUID


class Message(BaseModelWithUID):
    """
    This model is purely for prototyping.
    actual messaging will be done via the FastAPI 'chat_service' application, with ScyllaDB as the primary message DB 
    """
    
    # foreignkey fields
    author = models.ForeignKey(
        "core.User", on_delete=models.SET_NULL, related_name="messages"
    )
    author_uid = models.CharField(max_length=36, db_index=True, blank=True)

    channel = models.ForeignKey(
        "server.Channel", on_delete=models.CASCADE, related_name="channel_messages"
    )
    channel_uid = models.CharField(max_length=36, db_index=True, blank=True)

    thread = models.ForeignKey(
        "server.Thread", on_delete=models.CASCADE, related_name="thread_messages"
    )
    thread_uid = models.CharField(max_length=36, db_index=True, blank=True)

    # model fields 
    content = models.TextField(max_length=5000)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["channel_uid", "created_at"]),
            models.Index(fields=["thread_uid", "created_at"])
        ]

    def __str__(self):
        target = self.thread or self.channel
        return f"Message{self.uid} bu {self.author} in {target}"