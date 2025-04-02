from django.shortcuts import redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from fanlore.models import Event
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = reverse_lazy("event-list")

    def test_func(self):
        return self.request.user == self.get_object().creator

    def get(self, request, *args, **kwargs):
        return redirect("event-edit", pk=self.get_object().pk)
