from django.utils import timezone
from django.views.generic import ListView
from fanlore.models.event import Event
from django.utils.dateparse import parse_date
from datetime import datetime, time


class EventListView(ListView):
    model = Event
    template_name = "fanlore/event_list.html"
    context_object_name = "events"
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Event.objects.all()

        start_date_str = self.request.GET.get("start_date")
        end_date_str = self.request.GET.get("end_date")

        if start_date_str and end_date_str:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)

            if start_date and end_date:
                # Start at 00:00:00 and End at 23:59:59
                start_datetime = timezone.make_aware(
                    datetime.combine(start_date, time.min))
                end_datetime = timezone.make_aware(
                    datetime.combine(end_date, time.max))

                queryset = queryset.filter(
                    submission_start__gte=start_datetime,
                    submission_end__lte=end_datetime
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
