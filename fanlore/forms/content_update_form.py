from django import forms
from fanlore.models import Content


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  # Enable multiple file selection


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # Process multiple files correctly
        single_file_clean = super().clean
        if data is None:
            return []
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ContentUpdateForm(forms.ModelForm):
    content_files = MultipleFileField(label='Upload Files', required=False)

    class Meta:
        model = Content
        fields = ['title', 'description', 'topic_img', 'content_files', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure 'multiple' attribute for the file input
        self.fields['content_files'].widget.attrs['multiple'] = True