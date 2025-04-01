from django import forms
from django.contrib.auth import get_user_model
from pagedown.widgets import PagedownWidget
from fanlore.models import Content, Tag, Category

User = get_user_model()


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
    )

    class Meta:
        model = Content
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

        for name, field in self.fields.items():
            if not isinstance(field.widget, PagedownWidget):
                field.widget.attrs['class'] = 'form-control'

        self.fields['content_files'].widget.attrs['multiple'] = True

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