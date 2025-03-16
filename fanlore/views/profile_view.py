from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from fanlore.models import Content
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    A view to display a user's profile or a friend's profile.
    """
    template_name = "fanlore/profile.html"

    def get_context_data(self, **kwargs):
        """
        If a 'user_id' is provided in the URL, show that friend's profile.
        Otherwise, show the logged-in user's profile.
        """
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("user_id")

        if user_id:
            user = get_object_or_404(User, id=user_id)
        else:
            user = self.request.user  # Default to logged-in user

        context["user"] = user
        context["is_own_profile"] = user == self.request.user
        context["content_list"] = Content.objects.filter(collaborator=user)

        return context
