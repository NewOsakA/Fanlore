from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from fanlore.forms.achievement_form import AchievementFormSet
from fanlore.forms.event_create_form import EventCreateForm
from fanlore.models import Event, Achievement


class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View for creating a new event.
    Only the creator of the event can access this view.
    """
    model = Event
    form_class = EventCreateForm
    template_name = "fanlore/event_create.html"
    success_url = reverse_lazy("event-list")

    def get_context_data(self, **kwargs):
        """
        Add the achievement formset to the context.
        If the request is POST, bind it with request data;
        otherwise, provide an empty formset.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["achievement_formset"] = AchievementFormSet(
                self.request.POST, self.request.FILES,
                queryset=Achievement.objects.none()
            )
        else:
            context["achievement_formset"] = AchievementFormSet(
                queryset=Achievement.objects.none())
        return context

    def form_valid(self, form):
        """
        Handle a valid event form submission.
        Save the event and achievements only if form are valid.
        """
        context = self.get_context_data()
        achievement_formset = context["achievement_formset"]

        form.instance.creator = self.request.user
        self.object = form.save()

        if achievement_formset.is_valid():
            for achievement_form in achievement_formset:
                if achievement_form.cleaned_data:
                    achievement = achievement_form.save(commit=False)
                    achievement.event = self.object
                    achievement.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        """Restrict access to users marked as creators."""
        return self.request.user.is_creator
