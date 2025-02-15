from django.urls import path
from .views import (
    HomeView,
    CategoriesView,
    SearchView,
    CategoryItemsView,
    ItemView,
    NewItemView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("search/", SearchView.as_view(), name="search"),
    path(
        "category/<str:category_str>/",
        CategoryItemsView.as_view(),
        name="category_items",
    ),
    path("item/<slug:item_slug>/", ItemView.as_view(), name="item"),
    path("new-item/", NewItemView.as_view(), name="new_item"),
]
