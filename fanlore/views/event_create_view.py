from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from fanlore.models.event import Event
from fanlore.forms.event_create_form import EventCreateForm


class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventCreateForm
    template_name = "fanlore/event_create.html"
    success_url = reverse_lazy("event-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_creator
