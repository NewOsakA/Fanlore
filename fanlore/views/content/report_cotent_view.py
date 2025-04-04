from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from fanlore.models import Content, Report


class ReportContentView(LoginRequiredMixin, View):
    """
    Handle the submission of a report on a specific content item.
    Users must be logged in to report content.
    """

    def post(self, request, pk, *args, **kwargs):
        content = get_object_or_404(Content, pk=pk)
        topic = request.POST.get('topic')
        reason = request.POST.get('reason')

        if topic and reason:
            Report.objects.create(
                content=content,
                topic=topic,
                reason=reason,
                reported_by=request.user
            )
            messages.success(request, "✅ Your report has been submitted.")
        else:
            messages.error(request,
                           "⚠️ Please fill in all fields before submitting.")

        return redirect('view_post', pk=pk)
