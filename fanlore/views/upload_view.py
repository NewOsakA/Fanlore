from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ..models import Content, File
from ..forms.upload_content_form import ContentUploadForm

class ContentUploadView(LoginRequiredMixin, CreateView):
    model = Content
    form_class = ContentUploadForm
    template_name = 'fanlore/upload_content.html'
    success_url = reverse_lazy('content_list')
    login_url = '/signin'

    def form_valid(self, form):
        content = form.save(commit=False)
        content.collaborator = self.request.user
        content.save()

        # Manually handle multiple file uploads
        files = self.request.FILES.getlist('content_files')
        for uploaded_file in files:
            file_instance = File.objects.create(file=uploaded_file)
            content.content_files.add(file_instance)  # Link to Content model

        return super().form_valid(form)
