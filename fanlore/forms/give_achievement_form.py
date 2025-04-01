from django import forms
from fanlore.models import Achievement, UserAchievement
from django.contrib.auth import get_user_model

User = get_user_model()


class GiveAchievementForm(forms.Form):
    achievement_id = forms.IntegerField(widget=forms.HiddenInput)
    user_id = forms.IntegerField(widget=forms.HiddenInput)
    event_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean(self):
        cleaned_data = super().clean()
        achievement_id = cleaned_data.get("achievement_id")
        user_id = cleaned_data.get("user_id")
        event_id = cleaned_data.get("event_id")

        # Check achievement exists for this event
        if not Achievement.objects.filter(id=achievement_id, event__id=event_id).exists():
            raise forms.ValidationError("Invalid achievement for this event.")

        # Prevent duplicate achievements
        if UserAchievement.objects.filter(user_id=user_id, achievement_id=achievement_id).exists():
            raise forms.ValidationError("This user already has that achievement.")

        return cleaned_data
