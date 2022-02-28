from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.navigate, name="navigate" ),
    path("search/", views.search, name="search"),
    path("random", views.randomEntry, name="random"),
    path("add", views.newPage, name="add"),
    path("edit/<str:title>", views.editEntry, name="edit")
]