# views/event_create_view.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

from fanlore.models import Event, Achievement
from fanlore.forms.event_create_form import EventCreateForm
from fanlore.forms.achievement_form import AchievementFormSet


class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventCreateForm
    template_name = "fanlore/event_create.html"
    success_url = reverse_lazy("event-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["achievement_formset"] = AchievementFormSet(
                self.request.POST, self.request.FILES, queryset=Achievement.objects.none()
            )
        else:
            context["achievement_formset"] = AchievementFormSet(queryset=Achievement.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        achievement_formset = context["achievement_formset"]

        form.instance.creator = self.request.user
        self.object = form.save()

        if achievement_formset.is_valid():
            for achievement_form in achievement_formset:
                if achievement_form.cleaned_data:
                    achievement = achievement_form.save(commit=False)
                    achievement.event = self.object  # 💥 This line is crucial!
                    achievement.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        return self.request.user.is_creator
