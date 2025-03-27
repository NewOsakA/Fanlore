from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from fanlore.models import FriendRequest


class CancelFriendRequestView(LoginRequiredMixin, DeleteView):
    model = FriendRequest
    success_url = reverse_lazy("friends-list")

    def get_queryset(self):
        return FriendRequest.objects.filter(from_user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
