from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from fanlore.models import (
    Tag, Content, Bookmark, Report,
    Event, EventSubmission, Achievement, UserAchievement,
    Release, ContentFile, ReleaseFile, FriendRequest
)
from fanlore.models.category import Category

import uuid

User = get_user_model()


class BaseTestCase(TestCase):
    """Base test case for setting up common test data."""

    def setUp(self):
        """Set up the test data for users, content, and related models."""
        self.user = self.create_user("testuser", "test@example.com", "testpass123")
        self.other_user = self.create_user("otheruser", "other@example.com", "otherpass")
        self.creator = self.create_user("creator", "creator@example.com", "creatorpass", is_creator=True)

        self.user.follow(self.other_user)
        self.user.friends.add(self.other_user)

        self.tag = Tag.objects.create(name="test-tag")

        self.content = Content.objects.create(
            id=uuid.uuid4(),
            title="Sample Content",
            short_description="Short desc",
            description="**Some markdown**",
            creator=self.creator,
            category=Category.FANART,
            create_at=timezone.now()
        )
        self.content.tags.add(self.tag)
        self.content.collaborators.add(self.user)

        self.bookmark = Bookmark.objects.create(user=self.user, content=self.content)

        self.report = Report.objects.create(
            content=self.content,
            topic="Spam",
            reason="Inappropriate content",
            reported_by=self.user
        )

        self.event = Event.objects.create(
            creator=self.creator,
            title="Fan Challenge",
            short_description="Create your best fanart!",
            description="**Markdown event description**",
            submission_start=timezone.now(),
            submission_end=timezone.now() + timezone.timedelta(days=10),
            allow_text=True,
            allow_file=True,
            show_submissions=True
        )

        self.submission = EventSubmission.objects.create(
            event=self.event,
            user=self.user,
            text_response="Here's my submission!",
        )

        self.achievement = Achievement.objects.create(
            name="First Post!",
            description="Awarded for your first content submission.",
            event=self.event
        )

        self.user_achievement = UserAchievement.objects.create(
            user=self.user,
            achievement=self.achievement
        )

        self.release = Release.objects.create(
            title="v1.0",
            content=self.content,
            description="**Release notes**",
            updated_by=self.creator
        )

        self.content_file = ContentFile.objects.create(
            content=self.content
        )

        self.release_file = ReleaseFile.objects.create(
            release=self.release
        )

        self.friend_request = FriendRequest.objects.create(
            from_user=self.other_user,
            to_user=self.user
        )

    def create_user(self, username, email, password, **kwargs):
        """Create a user with the given parameters."""
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
