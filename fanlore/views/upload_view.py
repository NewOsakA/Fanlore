from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import cloudinary.uploader
from ..models import Content
from ..forms.upload_content_form import ContentUploadForm


class ContentUploadView(LoginRequiredMixin, CreateView):
    model = Content
    form_class = ContentUploadForm
    template_name = 'fanlore/upload_content.html'
    success_url = reverse_lazy('content_list')
    login_url = '/signin'

    def form_valid(self, form):
        content = form.save(commit=False)
        content.collaborator = self.request.user  # Associate with logged-in user
        content.save()

        # Handle the topic_img upload to Cloudinary
        topic_img = self.request.FILES.get('topic_img')
        print(f"Received topic_img: {topic_img}")

        if topic_img:
            try:
                # Open the file and upload
                with topic_img.open('rb') as file:
                    uploaded_image = cloudinary.uploader.upload(
                        file,
                        folder="content_images/",
                        public_id=str(content.id),
                        overwrite=True,
                        resource_type="image"
                    )
                    content.topic_img = uploaded_image.get("secure_url")
                    print(f"Topic image uploaded: {content.topic_img}")
            except Exception as e:
                print(f"Error uploading to Cloudinary: {e}")

        content.save()  # Save the content after assigning the image URL
        return super().form_valid(form)
