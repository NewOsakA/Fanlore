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
        widget=forms.TextInput(
            attrs={"placeholder": "Enter tags separated by commas",
                   "name": "tags"})
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
        fields = ['title', 'description', 'topic_img', 'category',
                  'collaborators']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.initial['tags'] = ', '.join(
                tag.name for tag in self.instance.tags.all())

        if self.user and self.instance.creator == self.user:
            self.fields['collaborators'].queryset = self.user.friends.all()
        else:
            self.fields.pop('collaborators', None)

        for name, field in self.fields.items():
            if not isinstance(field.widget, PagedownWidget):
                field.widget.attrs['class'] = 'form-control'

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
        content = super().save(commit=False)

        if commit:
            content.save()

            # Get tags from the form data
            tag_input = self.data.get('tags', '').strip()

            if tag_input:
                content.tags.clear()  # Clear previous tags
                tag_names = {t.strip() for t in tag_input.split(',') if
                             t.strip()}
                for tag_name in tag_names:
                    tag_obj, created = Tag.objects.get_or_create(
                        name=tag_name.title())
                    content.tags.add(tag_obj)

            self.save_m2m()

        return content
