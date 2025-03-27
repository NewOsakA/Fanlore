from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from fanlore.models import FriendRequest


class FriendRequestRejectView(LoginRequiredMixin, DeleteView):
    model = FriendRequest
    success_url = reverse_lazy("friends-list")

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)
