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
        fields = ['title', 'description', 'topic_img', 'category', 'tags',
                  'collaborators']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['collaborators'].queryset = self.user.friends.all()

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
        """Save content and handle tags"""
        content = super().save(commit=False)

        if commit:
            content.save()
            self.save_m2m()  # Handles tags and collaborators

            # Ensure tags are properly set (in case save_m2m didn't handle them)
            if 'tags' in self.cleaned_data:
                content.tags.set(self.cleaned_data['tags'])

        return content