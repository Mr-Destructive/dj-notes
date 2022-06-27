from django.urls import path
from . import views

app_name = "notebooks"

urlpatterns = [
    path("", views.NotebookListView.as_view(), name="notebook"),
    path("<int:pk>", views.NotebookDetailView.as_view(), name="notebook_view"),
    path("create/", views.NotebookCreateView.as_view(), name="create_notebook"),
    path("edit/<int:pk>", views.NotebookUpdateView.as_view(), name="update_book"),
    path("delete/<int:pk>", views.NotebookDeleteView.as_view(), name="delete_book"),
    path("addnote/<int:pk>", views.AddNote.as_view(), name="add_note"),
    path(
        "addnote-existing/<int:pk>",
        views.AddExistingNote.as_view(),
        name="add_existing_note",
    ),
]
