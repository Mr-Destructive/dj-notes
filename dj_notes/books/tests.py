from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from dj_notes.notes.forms import NoteForm
from dj_notes.notes.models import Note
from dj_notes.notes.views import NoteCreateView
from dj_notes.users.models import User

from .forms import AddNoteForm, NotebookForm
from .models import Notebook
from .views import (
    AddExistingNote,
    AddNote,
    NotebookCreateView,
    NotebookDeleteView,
    NotebookDetailView,
    NotebookListView,
    NotebookUpdateView,
)


class NotebookTest(TestCase):
    def setUp(self):
        book = {"name": "new book", "description": "description of notebook"}
        note = {"name": "new note", "content": "content of note"}
        self.book_data = book
        self.note_data = note
        author = User.objects.create(
            username="test",
            email="test@gmail.com",  # password1="12345678", password2="12345678"
        )
        author2 = User.objects.create(
            username="test2",
            email="test2@gmail.com",
        )
        self.author = author
        self.author2 = author2
        self.n = Note.objects.create(
            name=note["name"], content=note["content"], author=self.author
        )
        self.b = Notebook.objects.create(
            name=book["name"], description=book["description"], author=self.author
        )
        self.b1 = Notebook.objects.create(
            name=book["name"], description=book["description"], author=self.author
        )
        self.b2 = Notebook.objects.create(
            name="book 2", description=book["description"], author=self.author
        )
        self.b3 = Notebook.objects.create(
            name=book["name"], description=book["description"], author=self.author2
        )

    def create_book(self):

        book = self.book_data
        return Notebook.objects.create(
            name=book["name"], description=book["description"], author=self.author
        )

    def test_notebook_creation(self):
        w = self.create_book()
        self.assertTrue(isinstance(w, Notebook))
        self.assertEqual(w.__str__(), w.name)

    def test_book_detail_view(self):
        status_code = 200
        view_class = NotebookDetailView
        book = self.book_data
        b1_id = self.b1.id
        b2_id = self.b2.id
        b3_id = self.b3.id
        factory = RequestFactory()
        request = factory.get(reverse("notebooks:notebook_view", args=[b1_id]))
        request.user = self.author2
        self.assertRaises(
            PermissionDenied, view_class.as_view(), request=request, pk=b1_id
        )

        request = factory.get(reverse("notebooks:notebook_view", args=[b3_id]))
        request.user = self.author2
        response = view_class.as_view()(request, pk=b3_id)
        self.assertEqual(response.status_code, status_code)

    def test_book_list_view(self):
        status_code = 200
        view_class = NotebookListView
        factory = RequestFactory()
        request = factory.get(reverse("notebooks:notebook"))
        request.user = self.author
        response = view_class.as_view()(request)
        self.assertEqual(response.status_code, status_code)

    def test_book_update_view(self):
        view_class = NotebookUpdateView

        book = self.book_data
        book_id = self.b.id
        self.book_data["name"] = "updated book"
        factory = RequestFactory()
        request = factory.post(
            reverse(
                "notebooks:update_book",
                args=[
                    book_id,
                ],
            ),
            data=self.book_data,
        )
        request.user = self.author
        response = view_class.as_view()(request, pk=book_id)
        self.assertEqual(Notebook.objects.get(id=book_id).name, self.book_data["name"])

    def test_book_delete_view(self):
        view_class = NotebookDeleteView

        book = self.book_data
        book_id = self.b.id
        factory = RequestFactory()
        request = factory.delete(
            reverse(
                "notebooks:delete_book",
                args=[
                    book_id,
                ],
            ),
        )
        request.user = self.author
        response = view_class.as_view()(
            request,
            pk=book_id,
        )
        factory = RequestFactory()
        request = factory.get(reverse("notebooks:notebook_view", args=[book_id]))
        request.user = self.author

        self.assertRaises(
            Http404, NotebookDetailView.as_view(), request=request, pk=book_id
        )

    def test_create_book_view(self):
        view_class = NotebookCreateView
        factory = RequestFactory()
        request = factory.post(
            reverse("notebooks:create_notebook"), data=self.book_data
        )
        request.user = self.author
        response = NotebookCreateView.as_view()(request)
        self.assertEqual(Notebook.objects.last().name, self.book_data["name"])

    def test_valid_book_form(self):
        data = self.book_data
        form = NotebookForm(data=data)
        self.assertTrue(form.is_valid())

    def test_add_note_form(self):
        note = self.note_data
        form = AddNoteForm(data=note)
        self.assertTrue(form.is_valid())

    def test_add_note_view(self):
        data = self.book_data
        note = self.note_data
        factory = RequestFactory()
        book_id = self.b.id
        request = factory.post(
            reverse("notebooks:add_note", args=[book_id]),
            data=note,
        )
        request.user = self.author
        response = AddNote.as_view()(request, pk=book_id, data=note)
        note = Note.objects.latest("created")
        book_notes = Notebook.objects.get(id=book_id).notes.all().values()
        self.assertTrue(book_notes.filter(id=note.id).exists())

    def test_add_existing_note_view(self):
        data = self.book_data
        data["notes"] = self.note_data
        factory = RequestFactory()
        book_id = self.b.id
        request = factory.post(
            reverse("notebooks:add_existing_note", args=[book_id]),
            data=data,
        )
        request.user = self.author
        response = AddExistingNote.as_view()(request, pk=book_id)
        book_notes_author = Notebook.objects.get(id=book_id).notes.values_list(
            "author_id", flat=True
        )
        self.assertTrue(
            all(author_id == self.author.id for author_id in book_notes_author)
        )
