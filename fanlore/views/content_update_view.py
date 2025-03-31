import os

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import View
import cloudinary.uploader
from fanlore.models import Content, ContentFile
from fanlore.forms import ContentUpdateForm

class ContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'fanlore/content_edit.html'

    def get_object(self):
        return get_object_or_404(Content, pk=self.kwargs['pk'])

    def test_func(self):
        obj = self.get_object()
        return obj.collaborator == self.request.user

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        form = ContentUpdateForm(instance=obj)
        return render(request, self.template_name, {'form': form, 'content': obj})

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = ContentUpdateForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            content = form.save(commit=False)

            # Handle the topic_img upload to Cloudinary if a new image is uploaded
            topic_img = request.FILES.get('topic_img')
            if topic_img:
                try:
                    with topic_img.open('rb') as file:
                        uploaded_image = cloudinary.uploader.upload(
                            file,
                            folder="content_images/",
                            public_id=str(content.id),
                            overwrite=True,
                            resource_type="image"
                        )
                        content.topic_img = uploaded_image.get("secure_url")
                except Exception as e:
                    print(f"Error uploading topic image: {e}")

            # Handle file deletion for existing content files
            existing_files = ContentFile.objects.filter(content=content)
            delete_files = request.POST.getlist(
                'delete_files')  # List of file IDs to delete

            for file in existing_files:
                if str(file.id) in delete_files:
                    file.delete()  # Delete the file if it's in the delete list
                else:
                    # Save the files that were not deleted
                    if file.file not in request.FILES.getlist('content_files'):
                        file.save()

            # Handle the addition of new content files
            new_files = request.FILES.getlist('content_files')
            for uploaded_file in new_files:
                try:
                    filename, ext = os.path.splitext(
                        file.name)  # Extract base name and extension
                    public_id = f"{content.id}_{filename}"  # Avoid duplicate extensions

                    with uploaded_file.open('rb') as f:
                        uploaded_file = cloudinary.uploader.upload(
                            f,
                            folder="content_files/",
                            public_id=public_id,
                            overwrite=True,
                            resource_type="auto"
                        )
                        ContentFile.objects.create(
                            content=content,
                            file=uploaded_file.get("secure_url")
                        )
                except Exception as e:
                    print(f"Error uploading content file: {e}")

            content.save()

            return redirect(
                reverse_lazy('view_post', kwargs={'pk': content.pk}))

        return render(request, self.template_name,
                      {'form': form, 'content': obj})