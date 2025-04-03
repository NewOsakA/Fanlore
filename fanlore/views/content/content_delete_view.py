from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from fanlore.models import Content


class ContentDeleteView(LoginRequiredMixin, DeleteView):
    model = Content

    def get_object(self, queryset=None):
        return Content.objects.get(id=self.kwargs['content_id'])

    def get_success_url(self):
        return reverse_lazy('content_list')
