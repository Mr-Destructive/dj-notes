from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import TodoForm
from .models import Todo


class TodoView(View):
    model = Todo
    template_name = "todos/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todos"] = Todo.objects.filter(author=self.request.user).all()
        return context


class TodoSecureView(LoginRequiredMixin):
    model = Todo

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        user = request.user
        todo = self.object
        if not (todo.author == user or user.is_superuser):
            raise PermissionDenied
        return handler


class TodoListView(LoginRequiredMixin, TodoView, ListView):
    """View to list all todos."""

    template_name = "todos/todo_list.html"


class TodoDetailView(TodoSecureView, DetailView):
    """View to list the details from one todo."""

    template_name = "todos/todo_detail.html"


class TodoCreateView(LoginRequiredMixin, TodoView, CreateView):
    """View to create a new Todo"""

    form_class = TodoForm
    template_name = "todos/add_todo.html"
    success_url = "/todos"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TodoUpdateView(TodoSecureView, UpdateView):
    """View to update a Todo"""

    form_class = TodoForm
    template_name = "todos/edit_todo.html"
    success_url = "/todos"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = Todo.objects.get(id=self.kwargs["pk"])
        status = not self.object.completed
        Todo.objects.filter(id=self.kwargs["pk"]).update(completed=status)
        return redirect('todos:list-todos')


class TodoDeleteView(TodoSecureView, DeleteView):
    """View to delete a Todo"""

    template_name = "todos/delete_todo.html"
    success_url = "/todos"

def list_todos(request):
    todos = Todo.objects.filter(author=request.user).order_by("completed")
    context = {"todos": todos}
    return render(request, "todos/partials/list.html", context)
