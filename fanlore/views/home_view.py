from django.views.generic import ListView
from django.http import HttpResponse
from ..models import Content


class HomeView(ListView):
    """
    A view to display the homepage with a list of content.
    """
    model = Content  # Reference to the Content model
    template_name = "fanlore/home.html"  # Path to the template
    context_object_name = "content_list"  # Name of the context variable to be passed to the template

    def get_queryset(self):
        """
        Optionally filter or modify the queryset. By default, it fetches all content.
        """
        return Content.objects.all()  # Fetch all Content objects for now

    def home(request):
        """
        A simple view to return a message or redirect to the homepage.
        """
        return HttpResponse("Welcome to FanLore!")
