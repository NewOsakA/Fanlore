from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_to_remove = get_object_or_404(User, id=kwargs['user_id'])
        request.user.friends.remove(user_to_remove)
        user_to_remove.friends.remove(request.user)
        return redirect("friends-list")
