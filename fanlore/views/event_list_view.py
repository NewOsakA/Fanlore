from django.views.generic import ListView
from fanlore.models.event import Event


class EventListView(ListView):
    model = Event
    template_name = "fanlore/event_list.html"
    context_object_name = "events"
    ordering = ['-created_at']  # Newest first

    def get_queryset(self):
        return Event.objects.all()
