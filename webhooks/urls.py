from django.urls import path
from . import views

urlpatterns = [
    path(
        "server-update/", views.ServerUpdateView.as_view(), name="ServerUpdateView"
    ),  # Server Update (on push to GitHub)
]
