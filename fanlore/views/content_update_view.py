import os
<<<<<<< Updated upstream

import cloudinary.uploader
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

=======
import cloudinary.uploader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import View

from fanlore.models import Content, ContentFile
>>>>>>> Stashed changes
from fanlore.forms import ContentUpdateForm
from fanlore.models import Content, ContentFile, Tag


class ContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'fanlore/content_edit.html'

    def get_object(self):
        return get_object_or_404(Content, pk=self.kwargs['pk'])

    def test_func(self):
        obj = self.get_object()
<<<<<<< Updated upstream
        return (
                obj.creator == self.request.user or
                self.request.user in obj.collaborators.all()
        )
=======
        return obj.creator == self.request.user or obj.collaborators.filter(id=self.request.user.id).exists()
>>>>>>> Stashed changes

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        form = ContentUpdateForm(instance=obj, user=request.user)
        return render(request, self.template_name,
                      {'form': form, 'content': obj})

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = ContentUpdateForm(request.POST, request.FILES, instance=obj,
                                 user=request.user)

        if form.is_valid():
            content = form.save(commit=False)

<<<<<<< Updated upstream
            # Upload new cover image
=======
            # Handle the new topic_img upload (replace the old image)
>>>>>>> Stashed changes
            topic_img = request.FILES.get('topic_img')
            if topic_img:
                try:
                    uploaded_image = cloudinary.uploader.upload(
                        topic_img.read(),
                        folder="content_images/",
                        public_id=str(content.id),
                        overwrite=True,
                        resource_type="image"
                    )
                    content.topic_img = uploaded_image.get("secure_url")
                    print(f"DEBUG: Uploaded topic image {content.topic_img}")
                except Exception as e:
                    print(f"Error uploading topic image: {e}")

<<<<<<< Updated upstream
            # Handle new uploaded files
            for uploaded_file in request.FILES.getlist('content_files'):
                try:
                    filename, _ = os.path.splitext(uploaded_file.name)
                    public_id = f"{content.id}_{filename}"

                    uploaded_file_result = cloudinary.uploader.upload(
                        uploaded_file.read(),
                        folder="content_files/",
                        public_id=public_id,
                        overwrite=True,
                        resource_type="auto"
                    )

                    ContentFile.objects.create(
                        content=content,
                        file=uploaded_file_result.get("secure_url")
                    )
=======
            # Handle file deletion for existing content files
            existing_files = ContentFile.objects.filter(content=content)
            delete_files = request.POST.getlist(
                'delete_files')  # List of file IDs to delete

            for file in existing_files:
                if str(file.id) in delete_files:
                    try:
                        # Optionally delete the file from Cloudinary (if you need to)
                        # cloudinary.uploader.destroy(file.public_id)

                        file.delete()  # Delete the file from the database
                    except Exception as e:
                        print(f"Error deleting file: {e}")

            # Handle the addition of new content files
            new_files = request.FILES.getlist('content_files')
            for uploaded_file in new_files:
                try:
                    filename, ext = os.path.splitext(uploaded_file.name)
                    public_id = f"{content.id}_{filename}"  # Avoid duplicate extensions

                    with uploaded_file.open('rb') as f:
                        uploaded_file_data = cloudinary.uploader.upload(
                            f,
                            folder="content_files/",
                            public_id=public_id,
                            overwrite=True,
                            resource_type="auto"
                        )
                        ContentFile.objects.create(
                            content=content,
                            file=uploaded_file_data.get("secure_url")
                        )
>>>>>>> Stashed changes
                except Exception as e:
                    print(f"Error uploading content file: {e}")

            content.save()
            form.save_m2m()

            # Handle tags manually
            tag_input = request.POST.get('tags', '').strip()
            if tag_input:
                content.tags.clear()  # Clear previous tags
                tag_names = {t.strip() for t in tag_input.split(',') if
                             t.strip()}
                for tag_name in tag_names:
                    tag_obj, created = Tag.objects.get_or_create(
                        name=tag_name.title())
                    content.tags.add(tag_obj)
            return redirect('view_post', pk=content.pk)

<<<<<<< Updated upstream
        else:
            return render(request, self.template_name,
                          {'form': form, 'content': obj})
=======
        return render(request, self.template_name,
                      {'form': form, 'content': obj})
>>>>>>> Stashed changes
