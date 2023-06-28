from django.contrib import admin

from dj_notes.todos.models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    pass
