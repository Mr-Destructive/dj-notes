from django.db import models
from dj_notes.users.models import User
from dj_notes.utils.models import TimeStampedModel


class Note(TimeStampedModel):
    name = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name
