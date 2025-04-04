from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView

from fanlore.forms.event_submission_form import EventSubmissionForm
from fanlore.models import Event, EventSubmission


class EventSubmitView(FormView):
    """
    Handles creating or updating a submission for an event.
    - If a submission already exists for the user, it is updated.
    - If a submission does not exist, a new one is created.
    - If submissions are closed, redirects to the event detail page.
    """
    template_name = "fanlore/event_detail.html"
    form_class = EventSubmissionForm

    def dispatch(self, request, *args, **kwargs):
        """
        Retrieve the event and existing user submission.
        Prevent access if the event submission is closed.
        """
        self.event = get_object_or_404(Event, pk=kwargs["event_id"])
        self.user_submission = EventSubmission.objects.filter(
            event=self.event, user=request.user).first()

        if not self.event.is_open():
            messages.info(request, "Submissions are closed.")
            return redirect("event-detail", pk=self.event.id)

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Inject the event and the existing submission into the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs["event"] = self.event
        if self.user_submission:
            kwargs["instance"] = self.user_submission
        return kwargs

    def form_valid(self, form):
        """
        Save the submission and show a success message.
        """
        form.instance.event = self.event
        form.instance.user = self.request.user

        if self.user_submission:
            messages.success(self.request, "Submission updated successfully!")
        else:
            messages.success(self.request, "Submission created successfully!")

        form.save()
        return redirect("event-detail", pk=self.event.id)

    def get_success_url(self):
        """
        Redirect to the event detail page after submission.
        """
        return self.event.get_absolute_url()
