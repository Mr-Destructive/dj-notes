from datetime import datetime
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from dj_notes.books.models import Notebook
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


class NoteSecureView(LoginRequiredMixin):

    model = Note

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        user = request.user
        note = self.object
        if not (note.author == user or user.is_superuser):
            raise PermissionDenied
        return handler


class NotesListView(LoginRequiredMixin, NoteView, ListView):
    """View to list all notes."""

    template_name = "notes/note_list.html"


class NoteDetailView(NoteSecureView, DetailView):
    """View to list the details from one note."""

    template_name = "notes/note_detail.html"


class NoteCreateView(LoginRequiredMixin, NoteView, CreateView):
    """View to create a new Note"""

    form_class = NoteForm
    template_name = "notes/add_note.html"
    success_url = "/note"

    def form_valid(self, form):
        title_words = form.instance.name.split()
        if form.instance.name.startswith('!#') and len(title_words) < 5:
            form.instance.author = self.request.user
            book_name = form.instance.name.split('!#')[1]
            book = Notebook.objects.filter(author_id=self.request.user.id, name=book_name).first()
            if book:
                form.instance.name = datetime.now().strftime('%Y-%m-%d')
                response = super().form_valid(form)
                new_note = form.save(commit=False)
                #note = super(NoteCreateView, self).form_valid(form)
                new_note.save()
                book.notes.add(new_note)
                book.save()
                return response
            else:
                pass
                # Create a new book with the tag provided in the title and add the note
        else:
            return super(NoteCreateView, self).form_valid(form)


class NoteUpdateView(NoteSecureView, UpdateView):
    """View to update a Note"""

    form_class = NoteForm
    template_name = "notes/edit_note.html"
    success_url = "/note"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NoteUpdateView, self).form_valid(form)


class NoteDeleteView(NoteSecureView, DeleteView):
    """View to delete a Note"""

    template_name = "notes/delete_note.html"
    success_url = "/note"
