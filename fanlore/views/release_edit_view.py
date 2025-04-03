import logging
import os

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
import cloudinary.uploader
from ..models import Release, ReleaseFile
from ..forms import ReleaseForm

logger = logging.getLogger(__name__)


class ReleaseEditView(UpdateView):
    model = Release
    form_class = ReleaseForm
    template_name = 'fanlore/release_edit.html'
    context_object_name = 'release'

    def get_success_url(self):
        return reverse_lazy('view_post', kwargs={'pk': self.object.content.pk})

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            form.add_error(None, "You must be logged in to edit releases.")
            return self.form_invalid(form)

        # Save the form instance first
        response = super().form_valid(form)

        # Get the instance being updated
        release = self.object

        # Handle multiple file uploads
        release_files = self.request.FILES.getlist('release_files')
        for file in release_files:
            try:
                filename, _ = os.path.splitext(file.name)
                public_id = f"{release.id}_{filename}"

                # Upload the file to Cloudinary
                uploaded_file = cloudinary.uploader.upload(
                    file,  # No need to call file.read()
                    folder="release_files/",
                    public_id=public_id,
                    overwrite=True,
                    resource_type="auto"
                )
                file_url = uploaded_file.get("secure_url")

                # Save the file reference in the database
                ReleaseFile.objects.create(
                    release=release,  # Correct model reference
                    file=file_url  # Pass Cloudinary URL
                )
            except Exception as e:
                logger.error(f"Error uploading file {file.name}: {e}")
                messages.error(self.request, f"Failed to upload {file.name}")

        return response  # Return after processing files

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = self.object.content
        return context


