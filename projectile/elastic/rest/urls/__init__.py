from django.urls import path

from ..views.server import ServerSearchView

urlpatterns = [path("servers/", ServerSearchView.as_view(), name="search-servers")]
