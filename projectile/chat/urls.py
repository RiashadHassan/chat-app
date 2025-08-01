from django.urls import path

from chat.views import IndexView, ChatView

urlpatterns = [
    path("", IndexView.as_view(), name="chat-home"),
    path("<str:chat_type>/<uuid:chat_uid>/", ChatView.as_view(), name="chat-room"),
]
