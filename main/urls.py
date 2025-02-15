from django.urls import path
from .views import (
    HomeView,
    CategoriesView,
    SearchView,
    CategoryItemsView,
    ItemView,
    NewItemView,
    LinkView,
    SubmitLinkView,
    ReportLinkWorkingView,  # Add this import
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("search/", SearchView.as_view(), name="search"),
    path(
        "category/<slug:category_slug>/",
        CategoryItemsView.as_view(),
        name="category_items",
    ),
    path("item/<slug:item_slug>/", ItemView.as_view(), name="item"),
    path("new-item/", NewItemView.as_view(), name="new_item"),
    path("link/<int:link_id>/", LinkView.as_view(), name="link"),
    path("submit-link/", SubmitLinkView.as_view(), name="submit_link"),
    path("report-link-working/<int:link_id>/", ReportLinkWorkingView.as_view(), name="report_link_working"),
]
