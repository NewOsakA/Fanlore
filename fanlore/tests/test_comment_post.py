from django.urls import reverse
from fanlore.models import Content, Comment
from fanlore.tests.base import BaseTestCase


class ContentDetailViewTests(BaseTestCase):
    """Test cases for content detail view and comment functionality."""

    def setUp(self):
        """Set up content and URL for content detail view."""
        super().setUp()
        self.content = Content.objects.create(
            title="Commentable Post",
            description="Just content",
            category=1,
            creator=self.user
        )
        self.url = reverse("view_post", kwargs={"pk": self.content.pk})

    def test_comment_submission_success(self):
        """Test successful comment submission."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(self.url, data={
            "comment_text": "Nice post!"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

        comment = Comment.objects.first()
        self.assertEqual(comment.comment_text, "Nice post!")
        self.assertEqual(comment.commentator_name, self.user.username)
        self.assertEqual(comment.content, self.content)

    def test_invalid_comment_submission(self):
        """Test invalid comment submission with empty text."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(self.url, data={
            "comment_text": ""
        })

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "comment_text", "This field is required.")
        self.assertEqual(Comment.objects.count(), 0)

    def test_comments_displayed_on_page(self):
        """Test that comments are displayed on the content page."""
        Comment.objects.create(
            content=self.content,
            commentator_name="testuser",
            comment_text="Displayed comment"
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Displayed comment")

    def test_comment_default_avatar_used(self):
        """Test that default avatar is used for non-registered commentators."""
        Comment.objects.create(
            content=self.content,
            commentator_name="ghost",
            comment_text="I'm invisible"
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "default-avatar-url.jpg")

    def test_context_has_comment_form_and_comments(self):
        """Test that the context contains both comment form and comments."""
        self.client.login(username="testuser", password="testpass123")

        Comment.objects.create(
            content=self.content,
            commentator_name=self.user.username,
            comment_text="Testing form in context"
        )

        response = self.client.get(self.url)
        self.assertIn("form", response.context)
        self.assertIn("comments", response.context)
        self.assertContains(response, "Testing form in context")

    def test_comments_are_ordered_descending(self):
        """Test that comments are ordered by date in descending order."""
        self.client.login(username="testuser", password="testpass123")

        Comment.objects.create(
            content=self.content,
            commentator_name=self.user.username,
            comment_text="Older comment"
        )
        Comment.objects.create(
            content=self.content,
            commentator_name=self.user.username,
            comment_text="Newer comment"
        )

        response = self.client.get(self.url)
        comments = response.context["comments"]
        self.assertGreater(comments[0].comment_at, comments[1].comment_at)

    def test_multiple_comments_rendered(self):
        """Test that multiple comments are rendered on the page."""
        self.client.login(username="testuser", password="testpass123")

        Comment.objects.create(content=self.content, commentator_name=self.user.username, comment_text="First!")
        Comment.objects.create(content=self.content, commentator_name=self.user.username, comment_text="Second!")

        response = self.client.get(self.url)
        self.assertContains(response, "First!")
        self.assertContains(response, "Second!")

    def test_comment_form_reappears_on_invalid_post(self):
        """Test that the comment form reappears on invalid submission."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(self.url, data={"comment_text": ""})
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("comment_text", form.errors)

    def test_comment_submission_redirects_to_same_post(self):
        """Test that comment submission redirects back to the same post."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(self.url, data={"comment_text": "Redirect test"})
        self.assertRedirects(response, self.url)

    def test_comment_submission_on_deleted_content(self):
        """Test that comment submission fails with 404 when content is deleted."""
        self.content.delete()
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(self.url, data={"comment_text": "Test comment"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Comment.objects.count(), 0)
