from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Notebook
from .forms import NotebookForm, AddNoteForm


class NotebookView(View):
    model = Notebook

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = Notebook.objects.filter(author=self.request.user).all()
        return context


class NotebookListView(LoginRequiredMixin, NotebookView, ListView):
    """View to list all notes."""

    template_name = "books/book_list.html"


class NotebookDetailView(LoginRequiredMixin, NotebookView, DetailView):
    """View to list the details from one note."""

    template_name = "books/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = Notebook.objects.get(id=self.kwargs["pk"])
        return context


class NotebookCreateView(LoginRequiredMixin, NotebookView, CreateView):
    """View to create Notebook"""

    form_class = NotebookForm
    template_name = "books/create_notebook.html"
    success_url = "/books"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NotebookCreateView, self).form_valid(form)


class NotebookUpdateView(LoginRequiredMixin, NotebookView, UpdateView):
    """View to update a Notebook"""

    form_class = NotebookForm
    template_name = "books/edit_book.html"
    success_url = "/books"


class NotebookDeleteView(LoginRequiredMixin, NotebookView, DeleteView):
    """View to delete a Notebook"""

    template_name = "books/delete_book.html"
    success_url = "/books"


class AddNote(LoginRequiredMixin, NotebookView, CreateView):
    """Create a Note in a Book"""

    form_class = AddNoteForm
    template_name = "books/create_note.html"
    success_url = "/books"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AddNote, self).form_valid(form)
