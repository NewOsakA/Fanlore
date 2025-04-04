from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from fanlore.models import Content


class ContentDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to handle deletion of content by the creator or authorized user.
    """
    model = Content

    def get_object(self, queryset=None):
        """
        Retrieve the Content object based on the content_id URL parameter.
        """
        return Content.objects.get(id=self.kwargs['content_id'])

    def get_success_url(self):
        """
        After successful deletion, redirect the user to the content list page.
        """
        return reverse_lazy('content_list')
