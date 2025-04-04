from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse

from fanlore.models import FriendRequest

User = get_user_model()


class FriendRequestCreateView(LoginRequiredMixin, CreateView):
    """
    View for sending a friend request from the logged-in user to another user.
    It prevents duplicate requests and requests to already-added friends.
    """
    model = FriendRequest
    fields = []

    def form_valid(self, form):
        """
        Called when the form is valid.
        Ensures the request is not duplicated, or to an existing friend.
        """
        to_user = get_object_or_404(User, id=self.kwargs["user_id"])
        if to_user != self.request.user and not FriendRequest.objects.filter(
                from_user=self.request.user, to_user=to_user
        ).exists() and not self.request.user.friends.filter(
                id=to_user.id).exists():
            form.instance.from_user = self.request.user
            form.instance.to_user = to_user
            return super().form_valid(form)
        return super().form_invalid(form)

    def get_success_url(self):
        """
        Redirect to the referring page, or fallback to the friends list.
        """
        referer = self.request.META.get("HTTP_REFERER")
        return referer or reverse("friends-list")  # fallback just in case
