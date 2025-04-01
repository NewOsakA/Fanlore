from django.views.generic import ListView
from fanlore.models import Content, Category


class CategoryContentListView(ListView):
    model = Content
    template_name = "fanlore/category_contents.html"
    context_object_name = "content_list"
    paginate_by = 5

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Content.objects.filter(category=category_id).order_by("-create_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        context["category_name"] = dict(Category.choices).get(int(category_id), "Unknown Category")
        return context
