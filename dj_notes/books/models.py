from django.db import models
from django.contrib.postgres.fields import ArrayField
from dj_notes.users.models import User
from dj_notes.utils.models import TimeStampedModel
from dj_notes.notes.models import Note

class Tag(TimeStampedModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Notebook(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="book_writer"
    )
    notes = models.ManyToManyField(
        Note,
        related_name="booknotes",
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
            Tag,
            related_name="booktags",
            blank=True,
            null=True,
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name

