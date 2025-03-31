from django.contrib.auth import get_user_model
import random

User = get_user_model()


def recommended_friends(request):
    if request.user.is_authenticated:
        friends = request.user.friends.all()
        recommended = User.objects.exclude(id__in=friends).exclude(id=request.user.id)[:5]
    else:
        recommended = list(User.objects.all())
        random.shuffle(recommended)
        recommended = recommended[:5]
    return {'recommended_friends': recommended}
