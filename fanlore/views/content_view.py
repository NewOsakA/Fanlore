from django.views.generic import DetailView, FormView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from ..models import Content, Comment
from ..forms import CommentForm


class ContentDetailView(DetailView, FormView):
    model = Content
    template_name = 'fanlore/content_detail.html'
    context_object_name = 'content'
    form_class = CommentForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()  # Fetch related comments
        context['form'] = self.get_form()  # Add form to context
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
                reverse('content_detail', kwargs={'pk': self.object.pk}))

        return self.render_to_response(self.get_context_data(form=form))

