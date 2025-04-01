from django.views.generic import TemplateView


class HelpView(TemplateView):
    """
    A simple help page for users to find guidance and FAQs.
    """
    template_name = "fanlore/help.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["page_title"] = "Help & FAQs"
    #     return context
