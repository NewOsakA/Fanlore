from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from fanlore.tests.base import BaseTestCase
from fanlore.models import Content, ContentFile


class ContentUploadTests(BaseTestCase):
    """Test cases for uploading content functionality."""

    def setUp(self):
        """Set up the test data for content upload URL and valid data."""
        super().setUp()
        self.url = reverse("upload_content")
        self.valid_data = {
            "title": "Legend of Heroes",
            "short_description": "An epic tale of destiny",
            "description": "## A markdown intro",
            "category": 1,
        }

    def test_upload_content_success(self):
        """Test successful content upload."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(self.url, data=self.valid_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Content.objects.filter(title="Legend of Heroes").exists())

    def test_upload_requires_authentication(self):
        """Test that content upload requires authentication."""
        response = self.client.post(self.url, data=self.valid_data)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/signin", response.url)

    def test_missing_title_returns_error(self):
        """Test that missing title returns a validation error."""
        self.client.login(username="testuser", password="testpass123")
        data = self.valid_data.copy()
        data["title"] = ""

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "title", "This field is required.")

    def test_invalid_category_value(self):
        """Test that an invalid category value returns an error."""
        self.client.login(username="testuser", password="testpass123")
        data = self.valid_data.copy()
        data["category"] = 999

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "category",
                             "Select a valid choice. 999 is not one of the available choices.")

    def test_upload_content_with_tags(self):
        """Test that content upload works with tags."""
        self.client.login(username="testuser", password="testpass123")
        tag = self.tag
        data = self.valid_data.copy()
        data["tags"] = tag.name

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        content = Content.objects.get(title="Legend of Heroes")
        self.assertIn(tag.name.title(), [t.name for t in content.tags.all()])

    def test_upload_with_collaborators(self):
        """Test that collaborators are added to the content."""
        self.client.login(username="testuser", password="testpass123")
        data = self.valid_data.copy()
        data["collaborators"] = [self.other_user.id]

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        content = Content.objects.get(title="Legend of Heroes")
        self.assertIn(self.other_user, content.collaborators.all())

    def test_description_renders_markdown(self):
        """Test that markdown in description is rendered correctly."""
        self.client.login(username="testuser", password="testpass123")
        data = self.valid_data.copy()
        data["description"] = "# Markdown Header"

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        content = Content.objects.get(title="Legend of Heroes")
        self.assertIn("<h1>Markdown Header</h1>", content.description_rendered)

    def test_multiple_tags_created_and_associated(self):
        """Test that multiple tags are created and associated with content."""
        self.client.login(username="testuser", password="testpass123")
        data = self.valid_data.copy()
        data["tags"] = "fanart, lore ,  games"

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        content = Content.objects.get(title="Legend of Heroes")
        tag_names = [tag.name for tag in content.tags.all()]
        self.assertIn("Fanart", tag_names)
        self.assertIn("Lore", tag_names)
        self.assertIn("Games", tag_names)

    def test_empty_tags_input_is_handled(self):
        """Test that empty tag input is handled correctly."""
        self.client.login(username="testuser", password="testpass123")
        data = self.valid_data.copy()
        data["tags"] = ", , , ,"

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        content = Content.objects.get(title="Legend of Heroes")
        self.assertEqual(content.tags.count(), 0)

    def test_duplicate_tags_only_create_once(self):
        """Test that duplicate tags are not created."""
        self.client.login(username="testuser", password="testpass123")
        data = self.valid_data.copy()
        data["tags"] = "test-tag, Test-Tag"

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        content = Content.objects.get(title="Legend of Heroes")
        self.assertEqual(content.tags.count(), 1)

    def test_valid_collaborator_is_added(self):
        """Test that a valid collaborator is added to the content."""
        self.client.login(username="testuser", password="testpass123")

        self.user.friends.add(self.other_user)
        self.other_user.friends.add(self.user)

        data = self.valid_data.copy()
        data["collaborators"] = [self.other_user.id]

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        content = Content.objects.get(title="Legend of Heroes")
        self.assertIn(self.other_user, content.collaborators.all())

    def test_invalid_collaborator_shows_error(self):
        """Test that an invalid collaborator shows an error."""
        self.client.login(username="testuser", password="testpass123")

        unfriend = self.create_user(username="stranger", email="stranger@test.com", password="testpass123")

        data = self.valid_data.copy()
        data["collaborators"] = [unfriend.id]

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertIn("Select a valid choice", form.errors["collaborators"][0])

    def test_creator_is_set_correctly(self):
        """Test that the creator is set correctly on content upload."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)

        content = Content.objects.get(title="Legend of Heroes")
        self.assertEqual(content.creator, self.user)

    def test_content_file_upload_is_handled(self):
        """Test that content file upload is handled correctly."""
        self.client.login(username="testuser", password="testpass123")

        dummy_file = SimpleUploadedFile("doc.txt", b"filecontent", content_type="text/plain")
        mock_response = {"secure_url": "https://mocked-url.com/doc.txt"}

        data = {
            **self.valid_data,
            "content_files": [dummy_file]
        }

        with patch("cloudinary.uploader.upload", return_value=mock_response):
            response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 302)
        content = Content.objects.get(title="Legend of Heroes")
        self.assertTrue(ContentFile.objects.filter(content=content).exists())

    def test_multiple_file_uploads(self):
        """Test that multiple content files can be uploaded successfully."""
        self.client.login(username="testuser", password="testpass123")

        files = [
            SimpleUploadedFile("doc1.txt", b"data1", content_type="text/plain"),
            SimpleUploadedFile("doc2.txt", b"data2", content_type="text/plain"),
        ]

        mock_response = {"secure_url": "https://mocked-url.com/doc.txt"}

        with patch("cloudinary.uploader.upload", return_value=mock_response):
            data = {**self.valid_data, "content_files": files}
            response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 302)
        content = Content.objects.get(title="Legend of Heroes")
        self.assertEqual(ContentFile.objects.filter(content=content).count(), 2)
