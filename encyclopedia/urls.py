from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.pages, name="pages"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add")
]
