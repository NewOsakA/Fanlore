from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView

from fanlore.forms.event_submission_form import EventSubmissionForm
from fanlore.models import Event, EventSubmission


class EventSubmitView(FormView):
    template_name = "fanlore/event_detail.html"  # This will render the event detail again
    form_class = EventSubmissionForm

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs["event_id"])
        self.user_submission = EventSubmission.objects.filter(
            event=self.event, user=request.user).first()

        if not self.event.is_open():
            messages.info(request, "Submissions are closed.")
            return redirect("event-detail", pk=self.event.id)

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["event"] = self.event
        if self.user_submission:
            kwargs["instance"] = self.user_submission  # prefill for edit
        return kwargs

    def form_valid(self, form):
        form.instance.event = self.event
        form.instance.user = self.request.user

        if self.user_submission:
            messages.success(self.request, "Submission updated successfully!")
        else:
            messages.success(self.request, "Submission created successfully!")

        form.save()
        return redirect("event-detail", pk=self.event.id)

    def get_success_url(self):
        return self.event.get_absolute_url()
