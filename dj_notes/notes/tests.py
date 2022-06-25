from django.test import TestCase
from .models import Note
from dj_notes.users.models import User
from django.test import RequestFactory, TestCase
from .views import (
    NoteCreateView,
    NotesListView,
    NoteDetailView,
    NoteUpdateView,
    NoteDeleteView,
)
from .forms import NoteForm
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.http import Http404


class NoteTest(TestCase):
    def setUp(self):
        note = {"name": "new note", "content": "content of note"}
        self.note_data = note
        author = User.objects.create(
            username="test",
            email="test@gmail.com",
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
        self.n1 = Note.objects.create(
            name=note["name"], content=note["content"], author=self.author
        )
        self.n2 = Note.objects.create(
            name="note 2", content=note["content"], author=self.author
        )
        self.n3 = Note.objects.create(
            name=note["name"], content=note["content"], author=self.author2
        )

    def create_note(self):
        note = self.note_data

        return Note.objects.create(
            name=note["name"], content=note["content"], author=self.author
        )

    def test_note_creation(self):
        w = self.create_note()
        self.assertTrue(isinstance(w, Note))
        self.assertEqual(w.__str__(), w.name)

    def test_note_list_view(self):
        status_code = 200
        view_class = NotesListView
        note = self.note_data
        factory = RequestFactory()
        request = factory.get(reverse("notes:note"))
        request.user = self.author
        response = view_class.as_view()(request)
        self.assertEqual(response.status_code, status_code)

    def test_note_detail_view(self):
        status_code = 200
        view_class = NoteDetailView
        note = self.note_data
        n1_id = self.n1.id
        n2_id = self.n2.id
        n3_id = self.n3.id
        factory = RequestFactory()
        request = factory.get(reverse("notes:note_view", args=[n1_id]))
        request.user = self.author2
        self.assertRaises(
            PermissionDenied, view_class.as_view(), request=request, pk=n1_id
        )

        request = factory.get(reverse("notes:note_view", args=[n3_id]))
        request.user = self.author2
        response = view_class.as_view()(request, pk=n3_id)
        self.assertEqual(response.status_code, status_code)

    def test_note_create_view(self):
        view_class = NoteCreateView
        factory = RequestFactory()
        request = factory.post(reverse("notes:create_note"), data=self.note_data)
        request.user = self.author
        response = view_class.as_view()(request)
        self.assertEqual(Note.objects.last().name, self.note_data["name"])

    def test_valid_note_form(self):
        data = self.note_data
        form = NoteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_note_update_view(self):
        view_class = NoteUpdateView

        note = self.note_data
        note_id = self.n.id
        self.note_data["name"] = "updated note"
        factory = RequestFactory()
        request = factory.post(
            reverse("notes:update_note", args=[note_id]),
            data=self.note_data,
        )
        request.user = self.author
        response = view_class.as_view()(request, pk=note_id, data=self.note_data)
        self.assertEqual(Note.objects.get(id=note_id).name, self.note_data["name"])

    def test_note_delete_view(self):
        view_class = NoteDeleteView

        note = self.note_data
        note_id = self.n.id
        factory = RequestFactory()
        request = factory.delete(
            reverse(
                "notes:delete_note",
                args=[
                    note_id,
                ],
            ),
        )
        request.user = self.author
        response = view_class.as_view()(
            request,
            pk=note_id,
        )
        factory = RequestFactory()
        request = factory.get(reverse("notes:note_view", args=[note_id]))
        request.user = self.author

        self.assertRaises(
            Http404, NoteDetailView.as_view(), request=request, pk=note_id
        )
