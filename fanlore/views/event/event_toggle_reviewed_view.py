from django.http import HttpResponseRedirect
from django.views import View

from fanlore.models import EventSubmission


class ToggleReviewedView(View):
    """
    Toggle the reviewed status of a submission.
    Only the event creator is allowed to perform this action.
    """
    def post(self, request, pk):
        submission = EventSubmission.objects.get(pk=pk)
        if submission.event.creator == request.user:
            submission.reviewed = not submission.reviewed
            submission.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
