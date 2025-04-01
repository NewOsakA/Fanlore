from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_to_remove = get_object_or_404(User, id=kwargs['user_id'])

        # Remove friendship from both sides
        request.user.friends.remove(user_to_remove)
        user_to_remove.friends.remove(request.user)

        # Redirect to the referring page or fallback
        referer = request.META.get("HTTP_REFERER")
        return redirect(referer or "friends-list")
