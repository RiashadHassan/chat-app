from django.shortcuts import render

from django.views import View

class IndexView(View):
    template = "index.html" 
    def get(self, request, *args, **kwargs):
        return render(request, self.template)

class RoomView(View):
    template = "room.html"
    def get(self, request, *args, **kwargs):
        room_name = kwargs.get("room_name")
        context = {"room_name":room_name}
        return render(request, self.template, context)