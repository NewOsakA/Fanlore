from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView

from fanlore.forms import CommentForm
from fanlore.models import Content, Comment, Category, Bookmark, Release


class ContentDetailView(DetailView, FormView):
    """
    Combines DetailView and FormView to display content details and
    handle comment submissions.
    """
    model = Content
    template_name = 'fanlore/content_detail.html'
    context_object_name = 'content'
    form_class = CommentForm
    success_url = reverse_lazy('content_list')

    def get_context_data(self, **kwargs):
        """
        Add extra context for the template:
        - Categories
        - Comments and commenter images
        - Bookmark status
        - Associated releases
        """
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context["categories"] = Category.choices
        context["comments"] = Comment.objects.filter(
            content=self.object).order_by("-comment_at")
        context["releases"] = self.object.releases.all()

        # Check if the user is authenticated before checking bookmarks
        context["is_bookmarked"] = False
        if self.request.user.is_authenticated:
            context["is_bookmarked"] = Bookmark.objects.filter(
                user=self.request.user, content=self.object).exists()

        # Fetch user profile images for comments
        comments = context.get('comments')
        for comment in comments:
            user = get_user_model().objects.filter(
                username=comment.commentator_name).first()
            if user and user.profile_image:
                comment.user_profile_image = user.profile_image.url
            else:
                comment.user_profile_image = 'default-avatar-url.jpg'

        # Fetch the releases related to the content
        context["releases"] = Release.objects.filter(
            content=self.object).order_by('-create_at')

        # Include release-related information such as updated_by user
        for r in context["releases"]:
            r.updated_by_display_name = r.updated_by.username \
                if r.updated_by \
                else "Unknown"
            r.updated_by_profile_img = r.updated_by.profile_image.url \
                if r.updated_by and r.updated_by.profile_image \
                else 'default-avatar-url.jpg'

        return context

    def post(self, request, *args, **kwargs):
        """
        Handle comment form submission on the content detail page.
        """
        self.object = self.get_object()  # Get the content object
        form = self.get_form()

        if form.is_valid():
            comment = form.save(commit=False)
            comment.commentator_name = request.user.username
            comment.content = self.object  # Link to the content
            comment.save()
            return redirect(
                reverse('view_post', kwargs={'pk': self.object.pk}))

        return self.render_to_response(self.get_context_data(form=form))
