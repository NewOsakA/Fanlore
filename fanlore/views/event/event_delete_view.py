from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from fanlore.models import Event


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View to handle event deletion.
    Only the event creator is allowed to delete the event.
    """
    model = Event
    success_url = reverse_lazy("event-list")

    def test_func(self):
        """
        Ensure that only the creator of the event can delete it.
        """
        return self.request.user == self.get_object().creator

    def get(self, request, *args, **kwargs):
        """
        Redirect GET requests to the event edit page instead of showing a
        delete confirmation.
        """
        return redirect("event-edit", pk=self.get_object().pk)
