import cloudinary.uploader
from django import forms
from pagedown.widgets import PagedownWidget
from fanlore.models import Event
from django.core.files.uploadedfile import InMemoryUploadedFile


class EventCreateForm(forms.ModelForm):
    banner_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Banner Image"
    )

    class Meta:
        model = Event
        fields = ['title', 'short_description', 'banner_image', 'description',
                  'submission_start', 'submission_end', 'allow_text',
                  'allow_file', 'show_submissions']
        widgets = {
            'description': PagedownWidget(),
            'submission_start': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'}),
            'submission_end': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control'}),
        }

    def save(self, commit=True):
        event = super().save(commit=False)

        # Only upload a new image if a new one is uploaded
        if self.cleaned_data.get("banner_image") and isinstance(
                self.cleaned_data["banner_image"], InMemoryUploadedFile):
            uploaded = cloudinary.uploader.upload(
                self.cleaned_data["banner_image"],
                folder="event_banners/",
                public_id=f"event_{event.pk or 'new'}",
                overwrite=True,
                resource_type="image"
            )
            event.banner_image = uploaded.get('secure_url')

        if commit:
            event.save()
        return event
