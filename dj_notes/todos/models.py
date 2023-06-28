from django.db import models
from dj_notes.users.models import User

from dj_notes.utils.models import TimeStampedModel


class Todo(TimeStampedModel):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("completed", "-created",)
