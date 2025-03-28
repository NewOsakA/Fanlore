from django import forms

from fanlore.models.event_submission import EventSubmission


class EventSubmissionForm(forms.ModelForm):
    class Meta:
        model = EventSubmission
        fields = ['text_response', 'file_upload']

    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        super().__init__(*args, **kwargs)

        if not event.allow_text:
            self.fields.pop("text_response")
        if not event.allow_file:
            self.fields.pop("file_upload")

        # If both are removed, form will render empty
        if not self.fields:
            self.fields["invalid"] = forms.CharField(
                required=False,
                widget=forms.HiddenInput,
                initial="invalid"
            )

