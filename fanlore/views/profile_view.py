from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


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
        return context
