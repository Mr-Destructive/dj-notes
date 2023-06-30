import datetime
from django.http import HttpResponse
from django.shortcuts import render
from dj_notes.notes.models import Note

from dj_notes.todos.models import Todo
from . import app_settings


def index(request):
    context = {"notes": [], "todos": []}
    if request.user.is_authenticated:
        context["todos"] = Todo.objects.filter(author=request.user, created=datetime.date.today())
        context["notes"] = Note.objects.filter(author=request.user, created=datetime.date.today())
    return render(request, "base.html", context)

def service_worker(request):
    response = HttpResponse(
        open(app_settings.PWA_SERVICE_WORKER_PATH).read(),
        content_type="application/javascript",
    )
    return response


def manifest(request):
    return render(
        request,
        "manifest.json",
        {
            setting_name: getattr(app_settings, setting_name)
            for setting_name in dir(app_settings)
            if setting_name.startswith("PWA_")
        },
        content_type="application/json",
    )


def offline(request):
    return render(request, "offline.html")
