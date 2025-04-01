from django import forms
from pagedown.widgets import PagedownWidget
from django.contrib.auth import get_user_model
from ..models import Content, Tag, Category

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
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ContentUploadForm(forms.ModelForm):
    content_files = MultipleFileField(label='Upload Files', required=False)
    description = forms.CharField(widget=PagedownWidget())
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas",
        widget=forms.TextInput(attrs={"placeholder": "Enter tags separated by commas"})
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

    class Meta:
        model = Content
        fields = ['title', 'description', 'topic_img', 'category', 'tags', 'collaborators']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if current_user:
            # Assuming user.friends.all() returns the user's friends
            self.fields['collaborators'].queryset = current_user.friends.all()

        for name, field in self.fields.items():
            if not isinstance(field.widget, PagedownWidget):
                field.widget.attrs['class'] = 'form-control'

        self.fields['content_files'].widget.attrs['multiple'] = True

    def save(self, commit=True):
        content = super().save(commit=False)
        if commit:
            content.save()
            self.save_m2m()

            # Handle tags
            tag_input = self.cleaned_data['tags']
            if tag_input:
                tag_names = {t.strip() for t in tag_input.split(",") if t.strip()}
                for tag_name in tag_names:
                    formatted_name = tag_name.title()
                    tag = Tag.objects.filter(name__iexact=tag_name).first()
                    if not tag:
                        tag = Tag.objects.create(name=formatted_name)
                    content.tags.add(tag)

        return content
