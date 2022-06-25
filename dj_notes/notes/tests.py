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
        self.note_data = {"name": "new note", "content": "content of note"}

    def create_note(self):
        author = User.objects.create(
            username="test",
            email="test@gmail.com",  # password1="12345678", password2="12345678"
        )
        note = self.note_data

        return Note.objects.create(
            name=note["name"], content=note["content"], author=author
        )

    def test_note_creation(self):
        w = self.create_note()
        self.assertTrue(isinstance(w, Note))
        self.assertEqual(w.__str__(), w.name)

    def test_note_list_view(self):
        status_code = 200
        view_class = NotesListView
        user = User.objects.create(
            username="test",
            email="test@gmail.com",
        )
        user2 = User.objects.create(
            username="test2",
            email="test2@gmail.com",
        )
        note = self.note_data
        n1 = Note.objects.create(
            name=note["name"], content=note["content"], author=user
        )
        n2 = Note.objects.create(name="note 2", content=note["content"], author=user)
        n3 = Note.objects.create(
            name=note["name"], content=note["content"], author=user2
        )
        factory = RequestFactory()
        request = factory.get(reverse("notes:note"))
        request.user = user
        response = view_class.as_view()(request)
        self.assertEqual(response.status_code, status_code)

    def test_note_detail_view(self):
        status_code = 200
        view_class = NoteDetailView
        user = User.objects.create(
            username="test",
            email="test@gmail.com",
        )
        user2 = User.objects.create(
            username="test2",
            email="test2@gmail.com",
        )
        note = self.note_data
        n1 = Note.objects.create(
            name=note["name"], content=note["content"], author=user
        )
        n2 = Note.objects.create(name="note 2", content=note["content"], author=user)
        n3 = Note.objects.create(
            name=note["name"], content=note["content"], author=user2
        )
        n1_id = n1.id
        n2_id = n2.id
        n3_id = n3.id
        factory = RequestFactory()
        request = factory.get(reverse("notes:noteview", args=[n1_id]))
        request.user = user2
        self.assertRaises(
            PermissionDenied, view_class.as_view(), request=request, pk=n1_id
        )

        request = factory.get(reverse("notes:noteview", args=[n3_id]))
        request.user = user2
        response = view_class.as_view()(request, pk=n3_id)
        self.assertEqual(response.status_code, status_code)

    def test_note_create_view(self):
        view_class = NoteCreateView
        user = User.objects.create(
            username="test",
            email="test@gmail.com",
        )
        factory = RequestFactory()
        request = factory.post(reverse("notes:create_note"), data=self.note_data)
        request.user = user
        response = view_class.as_view()(request)
        self.assertEqual(Note.objects.last().name, self.note_data["name"])

    def test_valid_note_form(self):
        data = self.note_data
        author = User.objects.create(
            username="test",
            email="test@gmail.com",
        )
        n = Note.objects.create(
            name=data["name"], content=data["content"], author=author
        )
        form = NoteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_note_update_view(self):
        view_class = NoteUpdateView
        user = User.objects.create(
            username="test",
            email="test@gmail.com",
        )

        note = self.note_data
        n = Note.objects.create(name=note["name"], content=note["content"], author=user)
        note_id = n.id
        factory = RequestFactory()
        request = factory.put(
            reverse(
                "notes:update_note",
                args=[
                    note_id,
                ],
            ),
            data=self.note_data,
        )
        self.note_data["name"] = "updated note"
        request.user = user
        response = view_class.as_view()(request, pk=note_id, data=self.note_data)
        self.assertEqual(response.status_code, 200)

    def test_note_delete_view(self):
        view_class = NoteDeleteView
        user = User.objects.create(
            username="test",
            email="test@gmail.com",
        )

        note = self.note_data
        n = Note.objects.create(name=note["name"], content=note["content"], author=user)
        note_id = n.id
        factory = RequestFactory()
        request = factory.delete(
            reverse(
                "notes:delete_note",
                args=[
                    note_id,
                ],
            ),
        )
        request.user = user
        response = view_class.as_view()(
            request,
            pk=note_id,
        )
        factory = RequestFactory()
        request = factory.get(reverse("notes:noteview", args=[note_id]))
        request.user = user
        # resp = NoteDetailView.as_view()(request, pk=note_id)

        self.assertRaises(
            Http404, NoteDetailView.as_view(), request=request, pk=note_id
        )
