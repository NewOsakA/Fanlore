from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.shortcuts import get_object_or_404
from ..models import Content


class ContentDeleteView(LoginRequiredMixin, DeleteView):
    model = Content
    template_name = 'fanlore/content_confirm_delete.html'
    success_url = reverse_lazy('profile')  # Redirect to the profile page after deletion
    login_url = '/signin'

    def get_object(self, queryset=None):
        """
        Override get_object to ensure that the current user is the creator of the content.
        """
        content = get_object_or_404(Content, id=self.kwargs['content_id'])
        if content.collaborator != self.request.user:
            raise PermissionDenied("You are not authorized to delete this content.")
        return content
