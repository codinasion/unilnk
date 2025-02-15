from django.urls import path
from .views import HomeView, CategoriesView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("categories/", CategoriesView.as_view(), name="categories"),
]
