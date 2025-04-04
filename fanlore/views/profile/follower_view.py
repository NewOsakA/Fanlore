from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse

User = get_user_model()


class FollowUserView(LoginRequiredMixin, View):
    """
    Handles following a user.
    """
    def post(self, request: HttpRequest, user_id: int) -> HttpResponse:
        target_user = get_object_or_404(User, pk=user_id)
        request.user.follow(target_user)
        return redirect('friend-profile', user_id=user_id)


class UnfollowUserView(LoginRequiredMixin, View):
    """
    Handles unfollowing a user.
    """
    def post(self, request: HttpRequest, user_id: int) -> HttpResponse:
        target_user = get_object_or_404(User, pk=user_id)
        request.user.unfollow(target_user)
        return redirect('friend-profile', user_id=user_id)
