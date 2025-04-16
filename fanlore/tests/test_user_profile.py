from django.urls import reverse
from fanlore.tests.base import BaseTestCase
from fanlore.models import User
import uuid


class UserProfileTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password="testpass123")
        self.profile_url = reverse("profile")
        self.profile_edit_url = reverse("profile_edit")
        self.other_user = User.objects.create_user(
            username=f"otheruser_{uuid.uuid4().hex[:8]}",
            password="otherpass",
            display_name="Other User"
        )
        self.other_profile_url = reverse("friend-profile", kwargs={"user_id": self.other_user.id})

    def test_view_own_profile_page(self):
        """Test viewing your own profile page."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.display_name or self.user.username)

    def test_view_other_profile_page(self):
        """Test viewing another user's profile."""
        response = self.client.get(self.other_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.other_user.display_name)

    def test_edit_display_name(self):
        """Test that the user can update their display name."""
        response = self.client.post(self.profile_edit_url, {
            "display_name": "Updated Name",
            "bio": "Test bio",
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name or "",
            "last_name": self.user.last_name or "",
        }, follow=True)
        self.user.refresh_from_db()
        self.assertEqual(self.user.display_name, "Updated Name")

    def test_valid_bio(self):
        response = self.client.post(self.profile_edit_url, {
            "display_name": self.user.display_name or "Test",
            "bio": "This is a valid short bio.",
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name or "",
            "last_name": self.user.last_name or "",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, "This is a valid short bio.")

    def test_overly_long_bio(self):
        long_bio = "A" * 10001
        response = self.client.post(self.profile_edit_url, {
            "display_name": self.user.display_name or "Test",
            "bio": long_bio,
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name or "",
            "last_name": self.user.last_name or "",
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, long_bio)

    def test_blank_display_name(self):
        response = self.client.post(self.profile_edit_url, {
            "display_name": "",
            "bio": self.user.bio or "Bio",
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name or "",
            "last_name": self.user.last_name or "",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.display_name, "")  # blank is allowed per form

    def test_cannot_edit_other_user_profile(self):
        edit_other_url = reverse("profile_edit")
        self.client.logout()
        self.client.login(username=self.other_user.username, password="otherpass")
        response = self.client.post(edit_other_url, {
            "display_name": "Hacked Name",
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name or "",
            "last_name": self.user.last_name or "",
            "bio": "Malicious edit"
        }, follow=True)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.display_name, "Hacked Name")
        