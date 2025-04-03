from django.db.models.functions import Lower
from django.http import JsonResponse

from fanlore.models import Tag


def check_tag_existence(request):
    tag_names = request.GET.get('tags', '')
    tag_list = [tag.strip() for tag in tag_names.split(',') if tag.strip()]
    lower_tag_list = [tag.lower() for tag in tag_list]

    existing_tags_qs = Tag.objects.annotate(lower_name=Lower('name'))
    existing = set(
        existing_tags_qs.filter(lower_name__in=lower_tag_list).values_list(
            'lower_name', flat=True))

    result = [
        {
            "name": tag,
            "exists": tag.lower() in existing
        }
        for tag in tag_list
    ]
    return JsonResponse(result, safe=False)
