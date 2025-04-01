import os

import cloudinary.uploader
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from fanlore.forms import ContentUpdateForm
from fanlore.models import Content, ContentFile, Tag


class ContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'fanlore/content_edit.html'

    def get_object(self):
        return get_object_or_404(Content, pk=self.kwargs['pk'])

    def test_func(self):
        obj = self.get_object()
        return (
                obj.creator == self.request.user or
                self.request.user in obj.collaborators.all()
        )

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

            # Upload new cover image
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

        else:
            return render(request, self.template_name,
                          {'form': form, 'content': obj})
