from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

User = get_user_model()


class FriendListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "fanlore/friends_list.html"
    context_object_name = "all_users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("q", "").strip()

        # Retrieve user's friends
        friends = self.request.user.friends.all()

        # Filter friends based on search query
        added_friends = friends.filter(username__icontains=search_query) if search_query else friends

        # Filter users who are NOT friends
        non_friends = User.objects.exclude(id__in=friends).exclude(id=self.request.user.id)
        non_friends = non_friends.filter(username__icontains=search_query) if search_query else []

        # Add results to context
        context.update({
            "search_query": search_query,
            "added_friends": added_friends,
            "non_friends": non_friends,
        })
        return context
