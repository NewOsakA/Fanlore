from django.views.generic.edit import FormView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from fanlore.forms.give_achievement_form import GiveAchievementForm
from fanlore.models import Achievement, UserAchievement, User


class GiveAchievementView(FormView):
    form_class = GiveAchievementForm

    def form_valid(self, form):
        achievement = get_object_or_404(Achievement,
                                        id=form.cleaned_data["achievement_id"])
        user = get_object_or_404(User, id=form.cleaned_data["user_id"])

        # Create the achievement
        UserAchievement.objects.create(user=user, achievement=achievement)
        text = f"Achievement '{achievement.name}' given to {user.username}!"
        messages.success(self.request, text)
        return redirect(self.request.META.get("HTTP_REFERER", "/"))

    def form_invalid(self, form):
        # Show first validation error
        for error in form.errors.values():
            messages.error(self.request, error[0])
            break
        return redirect(self.request.META.get("HTTP_REFERER", "/"))
