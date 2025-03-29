from django import forms
from fanlore.models.event_submission import EventSubmission


class EventSubmissionForm(forms.ModelForm):
    class Meta:
        model = EventSubmission
        fields = ['text_response', 'file_upload']
        widgets = {
            'text_response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your text response here...'
            }),
            'file_upload': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'text_response': 'Text Response',
            'file_upload': 'Upload File',
        }

    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        super().__init__(*args, **kwargs)

        # Dynamically remove disallowed fields
        if not event.allow_text:
            self.fields.pop("text_response")
        if not event.allow_file:
            self.fields.pop("file_upload")

        # Prevent empty form rendering
        if not self.fields:
            self.fields["invalid"] = forms.CharField(
                required=False,
                widget=forms.HiddenInput,
                initial="invalid"
            )
