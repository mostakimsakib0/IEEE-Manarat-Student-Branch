from django.urls import path
from .views import EventCreateView, EventListView, gallery_view, DeleteEventView

urlpatterns = [
    path("create-event/", EventCreateView.as_view(), name="event_create"),
    path("event/list/", EventListView, name="event_gallery"),
    path("event/photo-gallery/", gallery_view, name="photo_gallery"),
    path("event/delete/<int:event_id>/", DeleteEventView, name="delete_event"),
]
