from django.urls import re_path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    # room is a place holder for channel_uid, thread_uid, group_chat_uid and direct_message_uid
    # re_path(r"ws/v1/chat/(?P<room_name>[^/]+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/v1/chat/(?P<chat_type>[^/]+)/(?P<uid>[^/]+)/$", ChatConsumer.as_asgi()),

]
