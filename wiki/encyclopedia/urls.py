from django.urls import path

from . import views

app_name = "encyclopedia"
# "app_name" helps to  correctly redirect to another url if there were
# different apps with same names

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.index),
    path("wiki/<str:title>", views.load_entry, name="load_entry"),
    path("search", views.search_entry, name="search_entry"),
    path("newPage", views.new_page, name="display_new"),
    path("validating", views.validating_data, name="validating"),
    path("randomChoice", views.random_page, name="random"),
    path("edit/<str:title>", views.edit_page, name="edit"),
    path("edition", views.edit_page_display, name="edition"),
    path("saving", views.save_changes, name="saving"),
    path("delete/<str:title>", views.delete_page, name="delete")
]
