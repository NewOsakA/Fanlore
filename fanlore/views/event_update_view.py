from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from fanlore.forms.event_create_form import EventCreateForm
from fanlore.models.event import Event


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventCreateForm
    template_name = "fanlore/event_edit.html"

    def get_success_url(self):
        return reverse_lazy('event-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.creator  # Only the creator can edit
