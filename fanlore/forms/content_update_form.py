from django import forms
<<<<<<< Updated upstream
from django.contrib.auth import get_user_model
from pagedown.widgets import PagedownWidget
from fanlore.models import Content, Tag, Category

User = get_user_model()
=======
from pagedown.widgets import PagedownWidget

from fanlore.models import Content, User, Category, Tag
>>>>>>> Stashed changes


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if data is None:
            return []
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return [single_file_clean(data, initial)]


class ContentUpdateForm(forms.ModelForm):
    content_files = MultipleFileField(label='Upload Files', required=False)
    description = forms.CharField(widget=PagedownWidget())
<<<<<<< Updated upstream
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas",
        widget=forms.TextInput(attrs={"placeholder": "Enter tags separated by commas", "name": "tags"})
    )
    category = forms.ChoiceField(choices=Category.choices, required=True)

    collaborators = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control", "style": "height: auto;"})
=======

    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter tags separated by commas",
            "class": "form-control",
            "value": lambda self: ', '.join(tag.name for tag in
                                            self.instance.tags.all()) if self.instance else ''
        })
    )
    category = forms.ChoiceField(
        choices=Category.choices,
        required=True,
        widget=forms.Select()
    )
    collaborators = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            "class": "form-control",
            "style": "height: auto;",
        })
    )
    topic_img = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
>>>>>>> Stashed changes
    )

    class Meta:
        model = Content
<<<<<<< Updated upstream
        fields = ['title', 'description', 'topic_img', 'category', 'collaborators']  # ⛔ Do NOT include 'tags' here

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Prepopulate tags if editing
        if self.instance and self.instance.pk:
            self.initial['tags'] = ', '.join(tag.name for tag in self.instance.tags.all())

        if self.user and self.instance.creator == self.user:
            self.fields['collaborators'].queryset = self.user.friends.all()
        else:
            self.fields.pop('collaborators', None)

=======
        fields = ['title', 'description', 'topic_img', 'category', 'tags',
                  'collaborators']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if current_user:
            self.fields['collaborators'].queryset = current_user.friends.all()

        # Properly initialize tags field with comma-separated names
        if self.instance and hasattr(self.instance, 'tags'):
            self.initial['tags'] = ', '.join(
                tag.name for tag in self.instance.tags.all())

        # Add form-control class to all fields except PagedownWidget
>>>>>>> Stashed changes
        for name, field in self.fields.items():
            if not isinstance(field.widget, PagedownWidget):
                field.widget.attrs['class'] = 'form-control'

        self.fields['content_files'].widget.attrs['multiple'] = True

<<<<<<< Updated upstream
    def save(self, commit=True):
=======
    def clean_tags(self):
        """Convert comma-separated tags to actual Tag objects"""
        tags_input = self.cleaned_data.get('tags', '')
        if not tags_input:
            return []

        # Split and clean tag names
        tag_names = [name.strip() for name in tags_input.split(',') if
                     name.strip()]

        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        return tags

    def save(self, commit=True):
        """Save the form and update tags"""
>>>>>>> Stashed changes
        content = super().save(commit=False)

        if commit:
            content.save()
<<<<<<< Updated upstream

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
=======
            self.save_m2m()  # Important for many-to-many fields

            # Clear existing tags and add new ones
            content.tags.clear()
            for tag in self.cleaned_data['tags']:
                content.tags.add(tag)
>>>>>>> Stashed changes

        return content