from django.urls import reverse
from fanlore.tests.base import BaseTestCase
from fanlore.models import Achievement, UserAchievement
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO


def generate_test_image():
    image = Image.new("RGB", (100, 100), color="blue")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return SimpleUploadedFile("badge.png", buffer.getvalue(), content_type="image/png")


class AchievementTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password="testpass123")
        self.profile_url = reverse("profile")

        self.achievement = Achievement.objects.create(
            name="Early Bird",
            description="Logged in before sunrise",
            icon=generate_test_image(),
        )

        UserAchievement.objects.create(
            user=self.user,
            achievement=self.achievement
        )

    def test_achievement_section_visible(self):
        """Achievements card section should appear on profile page."""
        response = self.client.get(self.profile_url)
        self.assertContains(response, "Achievements")

    def test_unlocked_badges_visible(self):
        """Unlocked badges should appear with proper alt text."""
        response = self.client.get(self.profile_url)
        self.assertContains(response, self.achievement.name)
        self.assertContains(response, self.achievement.description)

    def test_badge_hover_tooltip_visible(self):
        """Tooltip content for achievements appears in the DOM."""
        response = self.client.get(self.profile_url)
        self.assertContains(response, "achievement-tooltip")
        self.assertContains(response, self.achievement.description)

    def test_badge_image_hover_container(self):
        """Badges should be wrapped in the hover container div."""
        response = self.client.get(self.profile_url)
        self.assertContains(response, 'class="achievement-icon-container"')
        self.assertContains(response, f'alt="{self.achievement.name}"')
