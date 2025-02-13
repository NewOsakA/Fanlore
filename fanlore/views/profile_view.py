from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from fanlore.models import Content


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    A view to display the user's profile page.
    Only logged-in users can access this page.
    """
    template_name = "fanlore/profile.html"

    def get_context_data(self, **kwargs):
        """
        Add extra context to the template.
        """
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user

        # Fetch content created by the user
        context["content_list"] = Content.objects.filter(collaborator=self.request.user)

        return context

