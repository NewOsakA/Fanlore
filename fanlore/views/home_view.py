from django.views.generic import ListView
from django.db.models import Q
from ..models import Content, Category, Tag
from django.db import models


class HomeView(ListView):
    """
    A view to display the homepage with a list of content.
    """
    model = Content
    template_name = "fanlore/home.html"
    context_object_name = "content_list"
    paginate_by = 10

    def get_queryset(self):
        """
        Fetch content ordered by most recent, optionally filtered by a search query.
        """
        queryset = Content.objects.all().order_by('-create_at')
        query = self.request.GET.get("q")
        category = self.request.GET.get("category")

        if query:
            if query.startswith("#"):
                tag_name = query[1:]  # Remove the hash #
                queryset = queryset.filter(tags__name__iexact=tag_name)
            else:
                queryset = queryset.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(tags__name__icontains=query)
                ).distinct()

        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add categories and search query to the context.
        """
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.choices
        context["search_query"] = self.request.GET.get("q", "")
        context["current_category"] = self.request.GET.get("category")
        return context
