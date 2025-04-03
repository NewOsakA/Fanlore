from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from fanlore.models import Content, Category
from django.contrib.auth import get_user_model
from fanlore.models import UserAchievement, FriendRequest
from django.db.models import Q


User = get_user_model()


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    A view to display a user's profile or a friend's profile.
    """
    template_name = "fanlore/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("user_id")

        # Determine which user profile is being viewed
        if user_id:
            user = get_object_or_404(User, id=user_id)
        else:
            user = self.request.user

        # Friendship logic
        is_own_profile = user == self.request.user
        is_friend = user in self.request.user.friends.all()
        sent_request = FriendRequest.objects.filter(
            from_user=self.request.user,
            to_user=user).first()

        # Check following status
        is_following = self.request.user.following.filter(pk=user.pk).exists()

        # Add to context
        context.update({
            "user": user,
            "is_own_profile": is_own_profile,
            "is_friend": is_friend,
            "is_following": is_following,
            "has_sent_request": sent_request,
            "content_list": Content.objects.filter(
                Q(creator=user) | Q(collaborators=user))
            .distinct().order_by("-create_at"),
            "categories": Category.choices,
            "achievements": UserAchievement.objects.filter(user=user).order_by(
                "-date_earned"),
        })

        print(context["content_list"])

        return context
