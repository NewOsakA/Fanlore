from django import forms
from pagedown.widgets import PagedownWidget

from ..models import Release

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if data is None:
            return []
        single_file_clean = super().clean
        return [single_file_clean(d, initial) for d in data] if isinstance(
            data, (list, tuple)) else [single_file_clean(data, initial)]


class ReleaseForm(forms.ModelForm):
    release_files = MultipleFileField(label='Upload Files', required=False)
    description = forms.CharField(widget=PagedownWidget(), required=False)

    class Meta:
        model = Release
        fields = ["title", "description", "release_files"]

    def clean_description(self):
        """Ensure description is always a string"""
        description = self.cleaned_data.get("description", "")
        return description if description else ""

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.updated_by_id:
            raise ValueError("updated_by must be set before saving.")
        if commit:
            instance.save()
        return instance
