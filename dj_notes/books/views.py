from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from dj_notes.users.models import User

from dj_notes.notes.models import Note
from .models import Notebook
from .forms import NotebookForm, AddNoteForm, AddExistingNoteForm


class NotebookView(View):
    model = Notebook

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = Notebook.objects.filter(author=self.request.user).all()
        return context


class NotebookSecureView(LoginRequiredMixin):

    model = Notebook

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        user = request.user
        notebook = self.object
        if not (notebook.author == user or user.is_superuser):
            raise PermissionDenied
        return handler


class NotebookListView(LoginRequiredMixin, NotebookView, ListView):
    """View to list all notes."""

    template_name = "books/book_list.html"


class NotebookDetailView(NotebookSecureView, DetailView):
    """View to list the details from one note."""

    template_name = "books/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = Notebook.objects.get(id=self.kwargs["pk"])
        return context


class NotebookCreateView(NotebookView, CreateView):
    """View to create Notebook"""

    form_class = NotebookForm
    template_name = "books/create_notebook.html"
    success_url = "/books"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        user = self.request.user
        form.fields["notes"].queryset = Note.objects.filter(author=user)
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NotebookCreateView, self).form_valid(form)


class NotebookUpdateView(NotebookSecureView, UpdateView):
    """View to update a Notebook"""

    form_class = NotebookForm
    template_name = "books/edit_book.html"
    success_url = "/books"


class NotebookDeleteView(NotebookSecureView, DeleteView):
    """View to delete a Notebook"""

    template_name = "books/delete_book.html"
    success_url = "/books"


class AddNote(NotebookView, CreateView):
    """Create a Note in a Book"""

    form_class = AddNoteForm
    template_name = "books/create_note.html"
    success_url = "/books"

    def form_valid(self, form, **kwargs):
        form.instance.author = self.request.user
        response = super(AddNote, self).form_valid(form)
        book = Notebook.objects.get(id=self.kwargs["pk"])
        new_note = Note.objects.get(id=self.object.id)
        new_note.save()
        book.notes.add(new_note)
        book.save()
        return response


class AddExistingNote(NotebookSecureView, UpdateView):
    """Add an existing Note in a Book"""

    form_class = AddExistingNoteForm
    template_name = "books/add_existing_note.html"
    success_url = "/books"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        user = self.request.user
        form.fields["notes"].queryset = Note.objects.filter(author=user)
        return form
