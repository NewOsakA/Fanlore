import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from fanlore.models import Content, ContentLike


class LikeContentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            content_id = data.get("content_id")
            content = Content.objects.get(pk=content_id)
        except (KeyError, Content.DoesNotExist, json.JSONDecodeError):
            return JsonResponse({'success': False, 'error': 'Invalid data'},
                                status=400)

        like_obj = ContentLike.objects.filter(user=request.user,
                                              content=content).first()

        if like_obj:
            like_obj.delete()
            content.vote = max(content.vote - 1, 0)  # Prevent negative votes
            content.save()
            return JsonResponse({'success': True,
                                 'liked': False,
                                 'vote': content.vote})

        ContentLike.objects.create(user=request.user, content=content)
        content.vote += 1
        content.save()
        return JsonResponse({'success': True,
                             'liked': True,
                             'vote': content.vote})
