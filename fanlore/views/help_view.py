from django.views.generic import TemplateView


class HelpView(TemplateView):
    """
    A simple help page for users to find guidance and FAQs.
    """
    template_name = "fanlore/help.html"
