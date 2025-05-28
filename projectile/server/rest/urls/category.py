from django.urls import path
from ..views.category import CategoryListCreateView, CategoryDetailsView

urlpatterns = [
    path("", CategoryListCreateView.as_view(), name="category-list-create"),
    path(
        "<uuid:category_uid>/", CategoryDetailsView.as_view(), name="category-detials"
    ),
]
