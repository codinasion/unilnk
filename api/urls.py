from django.urls import path
from .views import CategoryApiView, ItemApiView

urlpatterns = [
    path("category/", CategoryApiView.as_view(), name="category_api"),
    path("item/", ItemApiView.as_view(), name="item_api"),
]
