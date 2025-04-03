from django.contrib.auth import get_user_model
from django.db.models import Count
import random
from fanlore.models import Tag


User = get_user_model()


def recommended_friends(request):
    if request.user.is_authenticated:
        friends = request.user.friends.all()
        recommended = User.objects.exclude(id__in=friends).exclude(
            id=request.user.id)[:5]
    else:
        recommended = list(User.objects.all())
        random.shuffle(recommended)
        recommended = recommended[:5]
    return {'recommended_friends': recommended}


def trending_tags(request):
    """
    Adds top 3 trending tags to all templates.
    """
    popular_tags = Tag.objects.annotate(
        post_count=Count("posts")).order_by("-post_count")[:3]
    return {"popular_tags": popular_tags}
