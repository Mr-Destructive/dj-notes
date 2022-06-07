from django import forms
from .models import Notebook
from dj_notes.notes.models import Note


class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        exclude = (
            "created",
            "updated",
            "author",
            # "notes",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Notebook Name",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Description",
                }
            ),
        }


class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = (
            "created",
            "updated",
            "author",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Note Name",
                }
            ),
            "content": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Content",
                }
            ),
        }
