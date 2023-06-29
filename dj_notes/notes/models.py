from django.db import models

from dj_notes.users.models import User
from dj_notes.utils.models import TimeStampedModel


class Tag(TimeStampedModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_tags"
    )

    def __str__(self):
        return self.name

class Note(TimeStampedModel):
    name = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="note_tags", blank=True, null=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name
