from django.contrib import admin

from dj_notes.books.models import Notebook
from dj_notes.notes.models import Tag

@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
