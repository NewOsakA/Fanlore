import logging
import os

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
import cloudinary.uploader

from fanlore.models import Content, Release, ReleaseFile  # Ensure ReleaseFile is imported
from fanlore.forms import ReleaseForm

logger = logging.getLogger(__name__)

class ReleaseCreateView(LoginRequiredMixin, FormView):
    template_name = "fanlore/add_release.html"
    model = Release
    form_class = ReleaseForm

    def dispatch(self, request, *args, **kwargs):
        """Ensure only creators or collaborators can access this view"""
        self.content = get_object_or_404(Content, pk=self.kwargs['content_id'])

        if request.user != self.content.creator and request.user not in self.content.collaborators.all():
            return redirect("view_post", pk=self.content.id)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Save the new release if the form is valid"""
        if not self.request.user.is_authenticated:
            return self.form_invalid(form)

        # Create an instance without saving
        release = form.instance
        release.updated_by = self.request.user
        release.content = self.content  # Ensure this is set correctly
        release.save()

        print(f"Release saved! Content ID: {release.content.id}")  # Debugging

        # Handle multiple file uploads (video or image)
        release_files = self.request.FILES.getlist('release_files')
        for file in release_files:
            try:
                filename, _ = os.path.splitext(file.name)
                public_id = f"{release.id}_{filename}"

                # Upload the file to Cloudinary
                uploaded_file = cloudinary.uploader.upload(
                    file.read(),
                    folder="release_files/",
                    public_id=public_id,
                    overwrite=True,
                    resource_type="auto"
                )
                file_url = uploaded_file.get("secure_url")

                # Create and save the ReleaseFile (inherits from File model)
                ReleaseFile.objects.create(
                    release=release,
                    # Correct field is 'release', not 'content'
                    file=file_url  # Pass the file URL
                )
            except Exception as e:
                logger.error(f"Error uploading file {file.name}: {e}")

        return redirect("view_post", pk=self.content.id)

    def get_context_data(self, **kwargs):
        """Pass the content object to the template"""
        context = super().get_context_data(**kwargs)
        context["content"] = self.content
        return context
