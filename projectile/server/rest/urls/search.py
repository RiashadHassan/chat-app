from django.urls import path

from ....elastic.rest.views.server import ServerSearchView

urlpatterns = [
    path("servers/", ServerSearchView.as_view()),
]