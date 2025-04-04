from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from fanlore.models import Release


class ReleaseDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to handle deleting a release.
    """
    model = Release

    def get_object(self, queryset=None):
        """
        Retrieve the specific release to be deleted.
        """
        return Release.objects.get(id=self.kwargs['release_id'])

    def get_success_url(self):
        """
        Redirect back to the content detail page after successful deletion.
        """
        return reverse_lazy('view_post', kwargs={'pk': self.object.content.id})
