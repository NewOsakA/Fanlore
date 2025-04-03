from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from fanlore.models import Bookmark, Content


class BookmarkedPostsView(LoginRequiredMixin, ListView):
    model = Content
    template_name = 'fanlore/bookmarked.html'
    context_object_name = 'content_list'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        bookmarked_posts = Bookmark.objects.filter(
            user=user).values_list('content', flat=True)
        return Content.objects.filter(id__in=bookmarked_posts)
