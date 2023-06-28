from django.urls import path

from . import views

app_name = "todos"

urlpatterns = [
    path("", views.TodoListView.as_view(), name="todos"),
    path("<int:pk>", views.TodoDetailView.as_view(), name="todo_view"),
    path("create/", views.TodoCreateView.as_view(), name="create_todo"),
    path("edit/<int:pk>", views.TodoUpdateView.as_view(), name="update_todo"),
    path("delete/<int:pk>", views.TodoDeleteView.as_view(), name="delete_todo"),
    path('list/', views.list_todos, name='list-todos'),
]
