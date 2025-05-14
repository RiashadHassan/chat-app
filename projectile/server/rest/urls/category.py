from django.urls import path
from ..views.category import CategoryListCreateView

urlpatterns = [
    path("", CategoryListCreateView.as_view(), name="category-list-create")
]
