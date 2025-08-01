from django.shortcuts import render

from django.views import View


class IndexView(View):
    template = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template)


class ChatView(View):
    template = "room.html"

    def get(self, request, *args, **kwargs):
        chat_type = kwargs.get("chat_type")
        chat_uid = kwargs.get("chat_uid")
        context = {"chat_type": chat_type, "chat_uid": chat_uid}
        return render(request, self.template, context)
