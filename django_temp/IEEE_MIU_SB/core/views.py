from django.shortcuts import render
from django.views import View
from Event.models import Event
from datetime import datetime
from Committee.models import WebDetails


class HomeView(View):
    def get(self, request):
        # events = Event.objects.all().order_by("-date") # if you want to show all events
        web_details = WebDetails.objects.first()
        if web_details:
            web_details.viewer_count += 1
            web_details.save()
        events = Event.objects.filter(is_featured=True).order_by("-date")[:5]
        return render(request, "index.html", {"events": events})


def current_year(request):
    return {"year": datetime.now().year}
