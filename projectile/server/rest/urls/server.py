from django.urls import path
from ..views.server import ServerListCreateView

urlpatterns = [
    path("", ServerListCreateView.as_view(), name="server-list-create")
]