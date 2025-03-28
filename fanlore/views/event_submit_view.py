from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView

from fanlore.forms.event_submission_form import EventSubmissionForm
from fanlore.models import Event, EventSubmission


class EventSubmitView(CreateView):
    model = EventSubmission
    form_class = EventSubmissionForm

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs["event_id"])
        if not self.event.is_open():
            return redirect("event-detail", pk=self.event.id)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["event"] = self.event
        return kwargs

    def form_valid(self, form):
        existing_submission = EventSubmission.objects.filter(
            event=self.event, user=self.request.user
        ).first()

        if existing_submission:
            messages.error(self.request,
                           "You have already submitted to this event.")
            return redirect(self.event.get_absolute_url())

        form.instance.event = self.event
        form.instance.user = self.request.user
        messages.success(self.request, "Submission successful!")
        return super().form_valid(form)

    def get_success_url(self):
        return self.event.get_absolute_url()
