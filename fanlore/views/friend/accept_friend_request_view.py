from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from fanlore.models import FriendRequest


class FriendRequestAcceptView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        friend_request = get_object_or_404(FriendRequest, pk=kwargs['pk'])

        if friend_request.to_user == request.user:
            print("Accepting:", friend_request.from_user.username)
            request.user.friends.add(friend_request.from_user)
            friend_request.delete()

        return redirect("friends-list")
