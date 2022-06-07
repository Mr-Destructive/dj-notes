from django.urls import path
from . import views

app_name = "notebooks"

urlpatterns = [
    path("", views.NotebookListView.as_view(), name="notebook"),
    path("create/", views.NotebookCreateView.as_view(), name="create_notebook"),
    path("<int:pk>", views.NotebookDetailView.as_view(), name="notebook_view"),
    path("edit/<int:pk>", views.NotebookUpdateView.as_view(), name="edit_book"),
    path("delete/<int:pk>", views.NotebookDeleteView.as_view(), name="delete_book"),
    path("addnote/<int:pk>", views.AddNote.as_view(), name="add_note"),
]
