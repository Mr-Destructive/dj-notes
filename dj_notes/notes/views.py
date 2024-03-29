import re
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from dj_notes.books.models import Notebook
from dj_notes.notes.templatetags.blog_markdown import convert_markdown
from dj_notes.todos.models import Todo

from .forms import NoteForm, TagForm
from .models import Note, Tag


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

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["tags"].queryset = Tag.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        title_words = form.instance.name.split()
        form.instance.author = self.request.user
        if form.instance.name.startswith("!#") and len(title_words) < 5:
            book_name = form.instance.name.split("!#")[1]
            book = Notebook.objects.filter(
                author_id=self.request.user.id, name=book_name
            ).first()
            form.instance.name = datetime.now().strftime("%Y-%m-%d")
            response = super().form_valid(form)
            new_note = form.save(commit=False)
            new_note.save()
            if book:
                book.notes.add(new_note)
            else:
                book = Notebook.objects.create(name=book_name, author=self.request.user)
            book.notes.add(new_note)
            book.save()
            return response
        pattern = re.compile(r'- \[(x|)\] (.*)')
        matches = pattern.finditer(form.instance.content)
        for match in matches:
            completed = bool(match.group(1))
            task = match.group(2).strip()
            todos = Todo.objects.filter(title=task, completed=False, author_id=self.request.user.id)
            if todos.count() == 0:
                Todo.objects.create(title=task, completed=completed, author_id=self.request.user.id)
            return super().form_valid(form)
        else:
            return super().form_valid(form)


class NoteUpdateView(NoteSecureView, UpdateView):
    """View to update a Note"""

    form_class = NoteForm
    template_name = "notes/edit_note.html"
    success_url = "/note"

    def form_valid(self, form):
        form.instance.author = self.request.user
        pattern = re.compile(r'- \[(x|)\] (.*)\r')
        matches = pattern.finditer(form.instance.content)
        for match in matches:
            completed = bool(match.group(1))
            task = match.group(2).strip()
            todos = Todo.objects.filter(title=task, completed=False, author_id=self.request.user.id)
            if todos.count() == 0:
                Todo.objects.create(title=task, completed=completed, author_id=self.request.user.id)
        return super().form_valid(form)


class NoteDeleteView(NoteSecureView, DeleteView):
    """View to delete a Note"""

    template_name = "notes/delete_note.html"
    success_url = "/note"


def note_preview(request):
    if request.method == "POST":
        markdown_content = request.POST.get("content")
        rendered_content = convert_markdown(markdown_content)
        print(rendered_content)
        context = {"preview": rendered_content}
        return render(request, "notes/partials/preview.html", context)
    else:
        return render(request, "notes/partials/preview.html", {})


class TagView(View):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TagCreateView(LoginRequiredMixin, TagView, CreateView):
    """View to add a tag to a Tag."""

    form_class = TagForm
    template_name = "notes/partials/add_tag.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
