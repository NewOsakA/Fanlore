import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Bookmark, Content

class ToggleBookmarkView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            content_id = data.get("content_id")

            if not content_id:
                return JsonResponse({"error": "Content ID is required."}, status=400)

            content = Content.objects.get(id=content_id)

            bookmark, created = Bookmark.objects.get_or_create(user=request.user, content=content)

            if not created:
                bookmark.delete()
                return JsonResponse({"bookmarked": False})

            return JsonResponse({"bookmarked": True})

        except Content.DoesNotExist:
            return JsonResponse({"error": "Content not found."}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
