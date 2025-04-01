from django.contrib.auth import get_user_model
from django.views.generic import DetailView, FormView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from ..models import Content, Comment, Category, Bookmark  # Import Bookmark model
from ..forms import CommentForm

class ContentDetailView(DetailView, FormView):
    model = Content
    template_name = 'fanlore/content_detail.html'
    context_object_name = 'content'
    form_class = CommentForm
    success_url = reverse_lazy('content_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context["categories"] = Category.choices
        context["comments"] = Comment.objects.filter(
            content=self.object).order_by("-comment_at")

        # ✅ Check if the user has bookmarked this content
        context["is_bookmarked"] = Bookmark.objects.filter(
            user=self.request.user, content=self.object).exists()

        # Fetch user profile images for comments
        comments = context.get('comments')
        for comment in comments:
            user = get_user_model().objects.filter(
                username=comment.commentator_name).first()
            comment.user_profile_image = user.profile_image.url if user and user.profile_image else 'default-avatar-url.jpg'

        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the content object
        form = self.get_form()

        if form.is_valid():
            comment = form.save(commit=False)
            comment.commentator_name = request.user.username  # Auto-assign username
            comment.content = self.object  # Link to the content
            comment.save()
            return redirect(
                reverse('view_post', kwargs={'pk': self.object.pk}))

        return self.render_to_response(self.get_context_data(form=form))
