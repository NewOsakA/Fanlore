from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from fanlore.forms.achievement_form import AchievementFormSet
from fanlore.forms.event_create_form import EventCreateForm
from fanlore.models import Event, Achievement


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to handle editing an existing event and its associated achievements.
    Only the event creator can access this view.
    """
    model = Event
    form_class = EventCreateForm
    template_name = "fanlore/event_edit.html"

    def get_success_url(self):
        """
        Redirect to the event detail page after a successful update.
        """
        return reverse_lazy('event-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """
        Add the AchievementFormSet to context for rendering in the template.
        Binds POST data if this is a form submission.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['achievement_formset'] = AchievementFormSet(
                self.request.POST, self.request.FILES,
                queryset=Achievement.objects.filter(event=self.object))
        else:
            context['achievement_formset'] = AchievementFormSet(
                queryset=Achievement.objects.filter(event=self.object))

        return context

    def form_valid(self, form):
        """
        Save the event and associated achievements if both
        the form and formset are valid.
        """
        context = self.get_context_data()
        formset = context['achievement_formset']
        form.instance.creator = self.request.user
        self.object = form.save()

        if formset.is_valid():
            for achievement_form in formset.forms:
                if achievement_form.cleaned_data.get('name'):
                    achievement = achievement_form.save(commit=False)
                    achievement.event = self.object
                    achievement.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        """
        Allow only the creator of the event to update it.
        """
        event = self.get_object()
        return self.request.user == event.creator
