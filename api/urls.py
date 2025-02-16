from django.urls import path
from .views import CategoryApiView

urlpatterns = [
    path("category/", CategoryApiView.as_view(), name="category_api"),
]
