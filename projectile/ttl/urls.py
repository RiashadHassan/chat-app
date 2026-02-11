from django.urls import path

from .views import TTLModelsListView

urlpatterns = [
    path("models/", TTLModelsListView.as_view(), name="ttl-models-list-view"),
]
