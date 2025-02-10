from django import forms
from ..models import Content


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  # Enable multiple file selection


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ContentUploadForm(forms.ModelForm):
    content_files = MultipleFileField(label='Upload Files', required=False)

    class Meta:
        model = Content
        fields = ['title', 'description', 'topic_img', 'content_files']
