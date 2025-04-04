from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from fanlore.models import Event, EventSubmission


class EventCreatorDashboardView(LoginRequiredMixin, ListView):
    """
    Dashboard view for event creators to manage and review submissions events.
    Only the creator of the event can access this view.
    """
    model = EventSubmission
    template_name = "fanlore/event_creator_dashboard.html"
    context_object_name = "submissions"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        """
        Ensure that only the creator of the event can access the dashboard.
        """
        self.event = Event.objects.get(pk=kwargs["event_id"])
        if self.event.creator != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Retrieve submissions for the event, with search, filter, and sort.
        """
        qs = EventSubmission.objects.filter(event=self.event).select_related(
            "user")
        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(user__username__icontains=search)

        review_filter = self.request.GET.get("review")
        if review_filter == "reviewed":
            qs = qs.filter(reviewed=True)
        elif review_filter == "unreviewed":
            qs = qs.filter(reviewed=False)

        sort = self.request.GET.get("sort")
        if sort == "oldest":
            qs = qs.order_by("submitted_at")
        else:
            qs = qs.order_by("-submitted_at")

        return qs

    def get_context_data(self, **kwargs):
        """
        Add context for the template, including search, filter, sort
        and submission counts.
        """
        context = super().get_context_data(**kwargs)
        submissions = self.get_queryset()

        context.update({
            "event": self.event,
            "search_query": self.request.GET.get("search", ""),
            "review_filter": self.request.GET.get("review", ""),
            "sort_order": self.request.GET.get("sort", "latest"),
            "remaining_reviews": submissions.filter(reviewed=False).count(),
            "total_submissions": submissions.count(),
        })
        return context
