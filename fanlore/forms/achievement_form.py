from django import forms
from django.forms import modelformset_factory
from fanlore.models import Achievement


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['name', 'description', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'rows': 2}),
        }


AchievementFormSet = modelformset_factory(
    Achievement,
    form=AchievementForm,
    extra=5,
    max_num=5,
    validate_max=True,
    can_delete=False
)
