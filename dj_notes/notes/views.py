from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Note
from .forms import NoteForm


class NoteView(View):
    model = Note
    template_name = "notes/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notes"] = Note.objects.filter(author=self.request.user).all()
        # context["notes"] = Note.objects.all()
        return context


class NotesListView(LoginRequiredMixin, NoteView, ListView):
    """View to list all notes."""

    template_name = "notes/note_list.html"


class NoteDetailView(LoginRequiredMixin, NoteView, DetailView):
    """View to list the details from one note."""

    template_name = "notes/note_detail.html"


class NoteCreateView(LoginRequiredMixin, NoteView, CreateView):
    """View to create a new Note"""

    form_class = NoteForm
    template_name = "notes/add_note.html"
    success_url = "/note"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NoteCreateView, self).form_valid(form)


class NoteUpdateView(LoginRequiredMixin, NoteView, UpdateView):
    """View to update a Note"""

    form_class = NoteForm
    template_name = "notes/edit_note.html"
    success_url = "/note"


class NoteDeleteView(LoginRequiredMixin, NoteView, DeleteView):
    """View to delete a Note"""

    template_name = "notes/delete_note.html"
    success_url = "/note"
