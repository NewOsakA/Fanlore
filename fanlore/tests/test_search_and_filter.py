from django.urls import reverse
from fanlore.models import Content, Category, Tag
from fanlore.tests.base import BaseTestCase


class SearchAndFilterTests(BaseTestCase):
    """Test cases for the home page content listing and filtering functionality."""

    def setUp(self):
        """Set up the test data for content, tags, and related models."""
        super().setUp()
        self.url = reverse("content_list")

        self.tag_art = Tag.objects.create(name="Art")
        self.tag_lore = Tag.objects.create(name="Lore")

        self.content1 = Content.objects.create(
            title="Dragon Lore",
            description="A deep dive into dragon myths",
            category=Category.LORE,
            creator=self.user
        )
        self.content1.tags.add(self.tag_lore)

        self.content2 = Content.objects.create(
            title="Epic FanArt",
            description="Stunning visuals from fans",
            category=Category.FANART,
            creator=self.user
        )
        self.content2.tags.add(self.tag_art)

        self.content3 = Content.objects.create(
            title="Random Story",
            description="Unrelated content",
            category=Category.GENERIC,
            creator=self.user
        )

    def test_homepage_shows_all_content(self):
        """Test that the homepage displays all content."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dragon Lore")
        self.assertContains(response, "Epic FanArt")
        self.assertContains(response, "Random Story")

    def test_search_by_title_keyword(self):
        """Test that content can be searched by title."""
        response = self.client.get(self.url, {"q": "Dragon"})
        self.assertContains(response, "Dragon Lore")
        self.assertNotContains(response, "Epic FanArt")

    def test_search_by_description_keyword(self):
        """Test that content can be searched by description."""
        response = self.client.get(self.url, {"q": "visuals"})
        self.assertContains(response, "Epic FanArt")
        self.assertNotContains(response, "Dragon Lore")

    def test_search_by_tag_keyword(self):
        """Test that content can be searched by tag."""
        response = self.client.get(self.url, {"q": "lore"})
        self.assertContains(response, "Dragon Lore")
        self.assertNotContains(response, "Epic FanArt")

    def test_search_by_hashtag(self):
        """Test that content can be searched by hashtag."""
        response = self.client.get(self.url, {"q": "#Art"})
        self.assertContains(response, "Epic FanArt")
        self.assertNotContains(response, "Dragon Lore")

    def test_filter_by_category(self):
        """Test that content can be filtered by category."""
        response = self.client.get(self.url, {"category": Category.LORE.value})
        self.assertContains(response, "Dragon Lore")
        self.assertNotContains(response, "Epic FanArt")
        self.assertNotContains(response, "Random Story")

    def test_search_and_filter_combined(self):
        """Test that search and filter can be combined."""
        response = self.client.get(self.url, {
            "q": "fan",
            "category": Category.FANART.value
        })
        self.assertContains(response, "Epic FanArt")
        self.assertNotContains(response, "Dragon Lore")

    def test_search_is_case_insensitive(self):
        """Test that search queries are case-insensitive."""
        response = self.client.get(self.url, {"q": "dragon"})
        self.assertContains(response, "Dragon Lore")

    def test_hashtag_search_case_insensitive(self):
        """Test that hashtag search queries are case-insensitive."""
        response = self.client.get(self.url, {"q": "#art"})
        self.assertContains(response, "Epic FanArt")

    def test_invalid_category_filter_returns_empty(self):
        """Test that an invalid category filter returns no results."""
        response = self.client.get(self.url, {"category": 999})
        self.assertNotContains(response, "Dragon Lore")
        self.assertNotContains(response, "Epic FanArt")
        self.assertNotContains(response, "Random Story")
        self.assertEqual(len(response.context["content_list"]), 0)

    def test_empty_search_query_returns_all(self):
        """Test that an empty search query returns all content."""
        response = self.client.get(self.url, {"q": ""})
        self.assertContains(response, "Dragon Lore")
        self.assertContains(response, "Epic FanArt")
        self.assertContains(response, "Random Story")

    def test_unknown_hashtag_returns_nothing(self):
        """Test that an unknown hashtag returns no results."""
        response = self.client.get(self.url, {"q": "#UnknownTag"})
        self.assertEqual(len(response.context["content_list"]), 0)

    def test_pagination_limits_results(self):
        """Test that pagination limits the number of results displayed."""
        for i in range(15):
            Content.objects.create(
                title=f"Extra Post {i}",
                description="More content",
                category=Category.GENERIC,
                creator=self.user
            )

        response = self.client.get(self.url)
        self.assertEqual(len(response.context["content_list"]), 10)

    def test_pagination_second_page(self):
        """Test that the second page of content is accessible."""
        for i in range(12):
            Content.objects.create(
                title=f"Page Test {i}",
                description="Pagination content",
                category=Category.GENERIC,
                creator=self.user
            )

        response = self.client.get(self.url, {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context["content_list"]), 0)

    def test_invalid_page_fallbacks(self):
        """Test that an invalid page number returns a 404 error."""
        response = self.client.get(self.url, {"page": "invalid"})
        self.assertEqual(response.status_code, 404)
