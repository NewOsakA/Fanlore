from django.urls import reverse
from django.utils import timezone
from fanlore.models import Event
from fanlore.tests.base import BaseTestCase


class EventCreationTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.creator.is_creator = True
        self.creator.save()
        self.client.login(username="creator", password="creatorpass")
        self.url = reverse("event-create")

    def test_all_valid_fields(self):
        """Test successful event creation with all valid inputs."""
        data = {
            "title": "Art Battle 2025",
            "short_description": "A new fan art challenge",
            "description": "Create your best original fanart!",
            "submission_start": timezone.now().date(),
            "submission_end": (timezone.now() + timezone.timedelta(days=5)).date(),
            "allow_text": True,
            "allow_file": True,
            "show_submissions": True
        }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(title="Art Battle 2025").exists())

    def test_missing_title(self):
        """Test event creation with missing title should fail."""
        data = {
            "title": "",
            "short_description": "Some desc",
            "description": "Some long markdown desc",
            "submission_start": timezone.now().date(),
            "submission_end": (timezone.now() + timezone.timedelta(days=5)).date(),
            "allow_text": True,
            "allow_file": True,
            "show_submissions": False
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_past_date_creation(self):
        """Test that an event with a past submission date is still accepted (form does not prevent it)."""
        past = timezone.now() - timezone.timedelta(days=5)
        data = {
            "title": "Past Event",
            "short_description": "Too late",
            "description": "Past tense vibes",
            "submission_start": past.strftime("%Y-%m-%dT%H:%M"),
            "submission_end": past.strftime("%Y-%m-%dT%H:%M"),
        }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(title="Past Event").exists())

    def test_empty_fields(self):
        """Test that submitting no data fails validation for required fields only."""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        required_fields = ["title", "description"]
        for field in required_fields:
            self.assertIn(field, form.errors)

    def test_special_characters_in_title(self):
        """Allow special characters in title (if permitted)."""
        data = {
            "title": "@#%!! FanArt *Battle*",
            "short_description": "Test case",
            "description": "Markdown ok?",
            "submission_start": timezone.now().date(),
            "submission_end": (timezone.now() + timezone.timedelta(days=2)).date(),
        }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(title__icontains="FanArt").exists())

    def test_max_description_length(self):
        """Test description at max allowed length (assume 5000)."""
        long_description = "A" * 5000
        data = {
            "title": "Long Description Event",
            "short_description": "Brief",
            "description": long_description,
            "submission_start": timezone.now().date(),
            "submission_end": (timezone.now() + timezone.timedelta(days=3)).date(),
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(title="Long Description Event").exists())

    def test_regular_user_cannot_create_event(self):
        """Test that a non-creator user cannot access event creation."""
        self.client.logout()
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_edit_existing_event(self):
        """Test that a creator can successfully update an event."""
        event = Event.objects.create(
            creator=self.creator,
            title="Old Title",
            short_description="Old desc",
            description="Old description",
            submission_start=timezone.now(),
            submission_end=timezone.now() + timezone.timedelta(days=3)
        )
        edit_url = reverse("event-edit", kwargs={"pk": event.pk})
        response = self.client.post(edit_url, {
            "title": "Updated Title",
            "short_description": "Updated",
            "description": "Updated desc",
            "submission_start": timezone.now().date(),
            "submission_end": (timezone.now() + timezone.timedelta(days=4)).date(),
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        event.refresh_from_db()
        self.assertEqual(event.title, "Updated Title")

    def test_delete_event_and_verify(self):
        """Test that an event can be deleted and is no longer listed."""
        event = Event.objects.create(
            creator=self.creator,
            title="Delete Me",
            submission_start=timezone.now(),
            submission_end=timezone.now() + timezone.timedelta(days=1)
        )
        delete_url = reverse("event-delete", kwargs={"pk": event.pk})
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Event.objects.filter(pk=event.pk).exists())

    def test_event_shows_in_profile_and_event_list(self):
        """Test that an event appears in creator dashboard and event list."""
        event = Event.objects.create(
            creator=self.creator,
            title="Dashboard Event",
            submission_start=timezone.now(),
            submission_end=timezone.now() + timezone.timedelta(days=2)
        )
        dashboard_url = reverse("event-creator-dashboard", kwargs={"event_id": event.pk})
        list_url = reverse("event-list")

        dash_response = self.client.get(dashboard_url)
        list_response = self.client.get(list_url)

        self.assertContains(dash_response, "Dashboard Event")
        self.assertContains(list_response, "Dashboard Event")