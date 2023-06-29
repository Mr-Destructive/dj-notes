from django import forms

from .models import Note, Tag


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ("created", "updated", "author")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Name",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 900px;",
                    "placeholder": "Content",
                }
            ),
            "tags": forms.CheckboxSelectMultiple(),
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ("description", "created", "updated", "user")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Tag Name",
                }
            ),
        }
