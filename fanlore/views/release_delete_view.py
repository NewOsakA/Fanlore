from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from fanlore.models import Release

class ReleaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Release

    def get_object(self, queryset=None):
        return Release.objects.get(id=self.kwargs['release_id'])

    def get_success_url(self):
        return reverse_lazy('view_post', kwargs={'pk': self.object.content.id})
