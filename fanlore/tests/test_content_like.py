import json
import uuid

from django.urls import reverse
from fanlore.models import Content, ContentLike
from fanlore.tests.base import BaseTestCase


class LikeContentTests(BaseTestCase):
    """Test cases for liking and unliking content."""

    def setUp(self):
        """Set up test content and login for the user."""
        super().setUp()
        self.client.login(username="testuser", password="testpass123")
        self.content = Content.objects.create(
            title="Likeable Post",
            description="Stuff",
            category=1,
            creator=self.user
        )
        self.url = reverse("like-content")

    def test_like_content_success(self):
        """Test that a user can successfully like content."""
        response = self.client.post(
            self.url,
            data=json.dumps({"content_id": str(self.content.id)}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContentLike.objects.count(), 1)
        self.assertEqual(Content.objects.get(pk=self.content.id).vote, 1)

        data = response.json()
        self.assertTrue(data["success"])
        self.assertTrue(data["liked"])
        self.assertEqual(data["vote"], 1)

    def test_unlike_content_success(self):
        """Test that a user can successfully unlike content."""
        ContentLike.objects.create(user=self.user, content=self.content)
        self.content.vote = 1
        self.content.save()

        response = self.client.post(
            self.url,
            data=json.dumps({"content_id": str(self.content.id)}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContentLike.objects.count(), 0)
        self.assertEqual(Content.objects.get(pk=self.content.id).vote, 0)

        data = response.json()
        self.assertTrue(data["success"])
        self.assertFalse(data["liked"])
        self.assertEqual(data["vote"], 0)

    def test_vote_does_not_go_below_zero(self):
        """Test that the vote count does not go below zero when unliking."""
        self.content.vote = 0
        self.content.save()

        response = self.client.post(
            self.url,
            data=json.dumps({"content_id": str(self.content.id)}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Content.objects.get(pk=self.content.id).vote, 1)

    def test_invalid_content_id_returns_error(self):
        """Test that an invalid content ID returns an error."""
        invalid_uuid = str(uuid.uuid4())

        response = self.client.post(
            self.url,
            data=json.dumps({"content_id": invalid_uuid}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_missing_content_id_returns_error(self):
        """Test that a missing content ID returns an error."""
        response = self.client.post(
            self.url,
            data=json.dumps({}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_invalid_json_body_returns_error(self):
        """Test that an invalid JSON body returns an error."""
        response = self.client.post(
            self.url,
            data="not-json",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_like_requires_authentication(self):
        """Test that liking content requires user authentication."""
        self.client.logout()
        response = self.client.post(
            self.url,
            data=json.dumps({"content_id": str(self.content.id)}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/signin", response.url)

    def test_double_like_does_not_create_duplicate(self):
        """Test that liking content twice by the same user does not create duplicates."""
        self.client.post(
            self.url,
            data=json.dumps({"content_id": str(self.content.id)}),
            content_type="application/json"
        )
        self.client.post(
            self.url,
            data=json.dumps({"content_id": str(self.content.id)}),
            content_type="application/json"
        )

        self.assertEqual(ContentLike.objects.filter(user=self.user, content=self.content).count(), 0)
        self.assertEqual(Content.objects.get(pk=self.content.id).vote, 0)
