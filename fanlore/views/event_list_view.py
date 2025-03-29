from django.utils import timezone
from django.views.generic import ListView

from fanlore.models.event import Event


class EventListView(ListView):
    model = Event
    template_name = "fanlore/event_list.html"
    context_object_name = "events"
    ordering = ['-created_at']

    def get_queryset(self):
        return Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()  # Pass current datetime
        return context
