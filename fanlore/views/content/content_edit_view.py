import os
import cloudinary.uploader
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from fanlore.models import Content, ContentFile
from fanlore.forms import ContentUpdateForm


class ContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'fanlore/content_edit.html'

    def get_object(self):
        return get_object_or_404(Content, pk=self.kwargs['pk'])

    def test_func(self):
        obj = self.get_object()
        return obj.creator == self.request.user or obj.collaborators.filter(
            id=self.request.user.id).exists()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        form = ContentUpdateForm(instance=obj, user=request.user)
        return render(request, self.template_name,
                      {'form': form, 'content': obj})

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = ContentUpdateForm(request.POST, request.FILES, instance=obj,
                                 user=request.user)

        if not form.is_valid():
            return render(request, self.template_name,
                          {'form': form, 'content': obj})

        content = form.save(commit=False)
        self._handle_cover_image(request, content)
        self._handle_file_operations(request, content)

        content.save()
        # Saves many-to-many relationships (including tags from the form)
        form.save_m2m()

        return redirect('view_post', pk=content.pk)

    def _handle_cover_image(self, request, content):
        """Handle cover image upload to Cloudinary"""
        topic_img = request.FILES.get('topic_img')
        if not topic_img:
            return

        try:
            uploaded_image = cloudinary.uploader.upload(
                topic_img.read(),
                folder="content_images/",
                public_id=str(content.id),
                overwrite=True,
                resource_type="image"
            )
            content.topic_img = uploaded_image.get("secure_url")
        except Exception as e:
            print(f"Error uploading topic image: {e}")

    def _handle_file_operations(self, request, content):
        """Handle file deletions and new uploads"""
        # Delete selected files
        self._delete_selected_files(request, content)

        # Upload new files
        self._upload_new_files(request, content)

    def _delete_selected_files(self, request, content):
        """Delete files marked for deletion"""
        delete_files = request.POST.getlist('delete_files')
        if not delete_files:
            return

        files_to_delete = ContentFile.objects.filter(
            content=content,
            id__in=delete_files
        )
        files_to_delete.delete()

    def _upload_new_files(self, request, content):
        """Upload new content files to Cloudinary"""
        for uploaded_file in request.FILES.getlist('content_files'):
            try:
                filename = os.path.splitext(uploaded_file.name)[0]
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
            except Exception as e:
                print(f"Error uploading content file: {e}")
