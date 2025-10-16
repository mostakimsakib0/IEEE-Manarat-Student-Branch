import os
from django.conf import settings
from urllib import request
from django.shortcuts import render,redirect
from .forms import EventForm
from .models import Event
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "event/event_form.html"
    success_url = reverse_lazy("event_create")


def EventListView(request):
    events = Event.objects.all().order_by("-date")
    return render(request, "event/event_gallery.html", {"events": events})


def DeleteEventView(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == "POST":
        event.delete()
        return redirect("event_gallery")
    return render(request, "event/event_gallery.html", {"event": event})


def gallery_view(request):
    image_urls = []

    event_image_path = os.path.join(settings.MEDIA_ROOT, "event_images")
    if os.path.exists(event_image_path):
        for root, dirs, files in os.walk(event_image_path):
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                    relative_path = os.path.relpath(
                        os.path.join(root, file), settings.MEDIA_ROOT
                    )
                    # Convert Windows backslashes to forward slashes
                    image_urls.append(
                        settings.MEDIA_URL + relative_path.replace("\\", "/")
                    )

    return render(request, "event/gallery.html", {"image_urls": image_urls})
