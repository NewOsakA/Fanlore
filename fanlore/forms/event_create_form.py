from django import forms
from pagedown.widgets import PagedownWidget
from fanlore.models import Event


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'submission_start', 'submission_end',
                  'allow_text', 'allow_file', 'show_submissions']
        widgets = {
            'description': PagedownWidget(),
            'submission_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'submission_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
