from django import forms
from pagedown.widgets import PagedownWidget

from fanlore.models import Content, User, Category, Tag


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


class ContentUpdateForm(forms.ModelForm):
    content_files = MultipleFileField(label='Upload Files', required=False)
    short_description = forms.CharField(
        required=False,
        help_text="A brief summary of your content.",
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Enter a short summary (optional)'
        }),
        max_length=300
    )
    description = forms.CharField(widget=PagedownWidget())
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter tags separated by commas",
            "class": "form-control"
        })
    )
    category = forms.ChoiceField(
        choices=Category.choices,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    collaborators = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            "class": "form-control",
            "style": "height: auto;"
        })
    )
    topic_img = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Content
        fields = ['title', 'short_description', 'description', 'topic_img',
                  'category', 'tags', 'collaborators']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            # Combine current friends + existing collaborators
            current_friends = self.user.friends.all()
            existing_collaborators = self.instance.collaborators.all()
            self.fields['collaborators'].queryset = (
                        current_friends | existing_collaborators).distinct()

        if self.instance.pk:
            self.initial['tags'] = ', '.join(
                tag.name for tag in self.instance.tags.all())

        for field in self.fields.values():
            if not isinstance(field.widget, PagedownWidget):
                field.widget.attrs.setdefault('class', 'form-control')

        self.fields['content_files'].widget.attrs['multiple'] = True

    def clean_tags(self):
        """Convert comma-separated tags to Tag objects"""
        tags_input = self.cleaned_data.get('tags', '')
        if not tags_input:
            return []

        tag_names = {name.strip() for name in tags_input.split(',') if
                     name.strip()}
        return [Tag.objects.get_or_create(name=name.title())[0] for name in
                tag_names]

    def save(self, commit=True):
        """Save content and handle tags and collaborators properly"""
        content = super().save(commit=False)

        if commit:
            content.save()
            self.save_m2m()

            # Handle tags
            if 'tags' in self.cleaned_data:
                content.tags.set(self.cleaned_data['tags'])

            # Preserve collaborators if the list is accidentally empty
            submitted_collaborators = self.cleaned_data.get('collaborators')
            if submitted_collaborators:
                content.collaborators.set(submitted_collaborators)
            else:
                # Optionally: Keep current collaborators or add current user
                content.collaborators.add(self.user)

        return content

