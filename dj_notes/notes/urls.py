from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("", views.NotesListView.as_view(), name="note"),
    path("<int:pk>", views.NoteDetailView.as_view(), name="note_view"),
    path("create/", views.NoteCreateView.as_view(), name="create_note"),
    path("edit/<int:pk>", views.NoteUpdateView.as_view(), name="update_note"),
    path("delete/<int:pk>", views.NoteDeleteView.as_view(), name="delete_note"),
    path("preview/", views.note_preview, name='note_preview'),

    path("create/tag", views.TagCreateView.as_view(), name="create_tag"),
]
