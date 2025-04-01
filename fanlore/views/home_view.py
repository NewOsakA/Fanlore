from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import render
from ..models import Content, Category


class HomeView(ListView):
    """
    A view to display the homepage with a list of content.
    """
    model = Content  # Reference to the Content model
    template_name = "fanlore/home.html"  # Path to the template
    context_object_name = "content_list"  # Name of the context variable to be passed to the template
    paginate_by = 10

    def get_queryset(self):
        """
        Optionally filter or modify the queryset. By default, it fetches all content.
        """
        return Content.objects.all().order_by('-create_at')  # Fetch all Content objects for now

    def get_context_data(self, **kwargs):
        """
        Add categories to the context data to pass them into the template.
        """
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.choices  # Pass the categories to the template
        return context

