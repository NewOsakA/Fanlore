from django.urls import reverse
from fanlore.models import Report
from fanlore.tests.base import BaseTestCase


class ReportContentTest(BaseTestCase):
    """Test cases for reporting content with various reasons."""

    def setUp(self):
        """Log in and set up the test content."""
        super().setUp()
        self.client.login(username="testuser", password="testpass123")
        self.url = reverse("view_post", kwargs={"pk": self.content.pk})
        self.form_url = reverse("report-content", kwargs={"pk": self.content.pk})
        self.payload_base = {
            "topic": "Spam"
        }

    def test_valid_reason(self):
        """Test that a valid report reason is accepted."""
        data = self.payload_base | {"reason": "Inappropriate material."}
        response = self.client.post(self.form_url, data=data, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Report.objects.count(), 2)

    def test_empty_reason(self):
        """Test that an empty reason does not create a report."""
        data = self.payload_base | {"reason": ""}
        response = self.client.post(self.form_url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Report.objects.count(), 1)

    def test_extremely_long_reason(self):
        """Test that a very long reason."""
        long_reason = "a" * 10001
        data = self.payload_base | {"reason": long_reason}
        response = self.client.post(self.form_url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_all_fields_blank(self):
        """Test that submitting a blank payload returns an error."""
        response = self.client.post(self.form_url, data={}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Report.objects.count(), 1)
