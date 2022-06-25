from django.test import TestCase
from dj_notes.notes.models import Note
from dj_notes.notes.views import NoteCreateView
from dj_notes.notes.forms import NoteForm
from dj_notes.users.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.http import Http404
from .models import Notebook
from .forms import NotebookForm, AddNoteForm
from .views import (
    NotebookCreateView,
    NotebookListView,
    NotebookDetailView,
    NotebookUpdateView,
    NotebookDeleteView,
    AddNote,
)


class NotebookTest(TestCase):
    def setUp(self):
        self.book_data = {"name": "new book", "description": "description of notebook"}
        self.note_data = {"name": "new note", "content": "content of note"}

    def create_book(self):
        author = User.objects.create(
            username="test",
            email="test@gmail.com",  # password1="12345678", password2="12345678"
        )

        book = self.book_data
        return Notebook.objects.create(
            name=book["name"], description=book["description"], author=author
        )

    def test_notebook_creation(self):
        w = self.create_book()
        self.assertTrue(isinstance(w, Notebook))
        self.assertEqual(w.__str__(), w.name)

    def test_book_detail_view(self):
        status_code = 200
        view_class = NotebookDetailView
        user = User.objects.create(
            username="test",
            email="test@gmail.com",
        )
        user2 = User.objects.create(
            username="test2",
            email="test2@gmail.com",
        )
        book = self.book_data
        b1 = Notebook.objects.create(
            name=book["name"], description=book["description"], author=user
        )
        b2 = Notebook.objects.create(
            name="book 2", description=book["description"], author=user
        )
        b3 = Notebook.objects.create(
            name=book["name"], description=book["description"], author=user2
        )
        b1_id = b1.id
        b2_id = b2.id
        b3_id = b3.id
        factory = RequestFactory()
        request = factory.get(reverse("notebooks:notebook_view", args=[b1_id]))
        request.user = user2
        self.assertRaises(
            PermissionDenied, view_class.as_view(), request=request, pk=b1_id
        )

        request = factory.get(reverse("notebooks:notebook_view", args=[b3_id]))
        request.user = user2
        response = view_class.as_view()(request, pk=b3_id)
        self.assertEqual(response.status_code, status_code)

    def test_book_list_view(self):
        status_code = 200
        view_class = NotebookListView
        user = User.objects.create(
            username="test",
            email="test@gmail.com",
        )
        user2 = User.objects.create(
            username="test2",
            email="test2@gmail.com",
        )
        book = self.book_data
        b1 = Notebook.objects.create(
            name=book["name"], description=book["description"], author=user
        )
        b2 = Notebook.objects.create(
            name="book 2", description=book["description"], author=user
        )
        b3 = Notebook.objects.create(
            name=book["name"], description=book["description"], author=user2
        )
        factory = RequestFactory()
        request = factory.get(reverse("notebooks:notebook"))
        request.user = user
        response = view_class.as_view()(request)
        self.assertEqual(response.status_code, status_code)

    def test_book_update_view(self):
        view_class = NotebookUpdateView
        user = User.objects.create(
            username="test",
            email="test@gmail.com",
        )

        book = self.book_data
        b = Notebook.objects.create(
            name=book["name"], description=book["description"], author=user
        )
        book_id = b.id
        self.book_data["name"] = "updated book"
        factory = RequestFactory()
        request = factory.put(
            reverse(
                "notebooks:edit_book",
                args=[
                    book_id,
                ],
            ),
            data=self.book_data,
        )
        request.user = user
        response = view_class.as_view()(request, pk=book_id, data=self.book_data)
        self.assertEqual(response.status_code, 200)

    def test_book_delete_view(self):
        view_class = NotebookDeleteView
        user = User.objects.create(
            username="test",
            email="test@gmail.com",
        )

        book = self.book_data
        b = Notebook.objects.create(
            name=book["name"], description=book["description"], author=user
        )
        book_id = b.id
        factory = RequestFactory()
        request = factory.delete(
            reverse(
                "notebooks:delete_book",
                args=[
                    book_id,
                ],
            ),
        )
        request.user = user
        response = view_class.as_view()(
            request,
            pk=book_id,
        )
        factory = RequestFactory()
        request = factory.get(reverse("notebooks:notebook_view", args=[book_id]))
        request.user = user
        # resp = NoteDetailView.as_view()(request, pk=book_id)

        self.assertRaises(
            Http404, NotebookDetailView.as_view(), request=request, pk=book_id
        )

    def test_create_book_view(self):
        view_class = NotebookCreateView
        user = User.objects.create(
            username="test",
            email="test@gmail.com",
        )
        factory = RequestFactory()
        request = factory.post(
            reverse("notebooks:create_notebook"), data=self.book_data
        )
        request.user = user
        response = NotebookCreateView.as_view()(request)
        self.assertEqual(Notebook.objects.last().name, self.book_data["name"])

    def test_valid_book_form(self):
        data = self.book_data
        author = User.objects.create(
            username="test",
            email="test@gmail.com",
        )

        b = Notebook.objects.create(
            name=data["name"], description=data["description"], author=author
        )
        form = NotebookForm(data=data)
        self.assertTrue(form.is_valid())

    def test_book_add_note_form(self):
        data = self.book_data
        author = User.objects.create(
            username="test",
            email="test@gmail.com",
        )
        b = Notebook.objects.create(
            name=data["name"], description=data["description"], author=author
        )

        note = self.note_data
        n = Note.objects.create(
            name=note["name"], content=note["content"], author=author
        )
        form = AddNoteForm(data=note)
        self.assertTrue(form.is_valid())

    def test_book_add_note_view(self):
        data = self.book_data
        author = User.objects.create(
            username="test",
            email="test@gmail.com",
        )
        b = Notebook.objects.create(
            name=data["name"], description=data["description"], author=author
        )

        note = self.note_data
        factory = RequestFactory()

        book_id = b.id
        data["notes"] = [
            note,
        ]
        data["author"] = author
        request = factory.post(
            reverse("notebooks:add_note", args=[book_id]),
            data=note,
        )
        request.user = author
        response = AddNote.as_view()(request, pk=book_id, data=note)
        note = Note.objects.last()
        book_notes = Notebook.objects.get(id=book_id).notes.all().values()

        self.assertTrue(book_notes.filter(id=note.id).exists())
