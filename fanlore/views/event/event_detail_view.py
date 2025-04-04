from django.utils import timezone
from django.views.generic.detail import DetailView
from fanlore.models import Event, EventSubmission, Achievement
from fanlore.forms.event_submission_form import EventSubmissionForm


class EventDetailView(DetailView):
    """
    Display the details of a specific event, including:
    - Whether the event is open
    - If the current user can submit
    - The user’s existing submission (if any)
    - Submissions
    - Achievements
    """
    model = Event
    template_name = "fanlore/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        user = self.request.user
        now = timezone.now()

        is_open = event.is_open()
        can_submit = is_open and (event.allow_text or event.allow_file)
        has_started = event.submission_start \
            is None or event.submission_start <= now
        has_ended = event.submission_end \
            is not None and event.submission_end < now
        is_creator = user.is_authenticated and user == event.creator

        user_submission = None
        if user.is_authenticated:
            user_submission = EventSubmission.objects.filter(
                event=event,
                user=user).first()

        show_submissions = event.show_submissions or is_creator
        submissions = event.submissions.all() if show_submissions else []

        submission_form = None

        if can_submit and user.is_authenticated:
            if user_submission:
                submission_form = EventSubmissionForm(instance=user_submission,
                                                      event=event)
            else:
                submission_form = EventSubmissionForm(event=event)

        achievements = Achievement.objects.filter(event=event)

        context.update({
            "is_open": is_open,
            "can_submit": can_submit,
            "has_started": has_started,
            "has_ended": has_ended,
            "is_creator": is_creator,
            "user_submission": user_submission,
            "submissions": submissions,
            "submission_form": submission_form,
            "show_submissions": show_submissions,
            "achievements": achievements,
        })
        return context
