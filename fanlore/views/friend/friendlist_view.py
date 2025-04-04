from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from fanlore.models import FriendRequest, Category

User = get_user_model()


class FriendListView(LoginRequiredMixin, ListView):
    """
    Displays the friend list page, including:
    - Added friends
    - Users not yet added
    - Incoming friend requests
    - Search functionality
    """
    model = User
    template_name = "fanlore/friends_list.html"
    context_object_name = "all_users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("q", "").strip()

        friends = self.request.user.friends.all()
        added_friends = friends.filter(
            username__icontains=search_query) if search_query else friends

        non_friends = User.objects.exclude(id__in=friends).exclude(
            id=self.request.user.id)
        non_friends = non_friends.filter(
            username__icontains=search_query) if search_query else []
        context.update({
            "search_query": search_query,
            "added_friends": added_friends,
            "non_friends": non_friends,
            "incoming_requests": FriendRequest.objects.filter(
                to_user=self.request.user),
            "sent_requests": FriendRequest.objects.filter(
                from_user=self.request.user),
            "sent_user_ids": set(FriendRequest.objects.filter(
                from_user=self.request.user).values_list("to_user_id",
                                                         flat=True)),
        })
        context["categories"] = Category.choices

        return context
