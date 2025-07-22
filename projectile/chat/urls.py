from django.urls import path

from chat.views import IndexView, RoomView

urlpatterns = [
    path("", IndexView.as_view(), name="chat-home"),
    path("<str:room_name>/", RoomView.as_view(), name="chat-room"),
]
