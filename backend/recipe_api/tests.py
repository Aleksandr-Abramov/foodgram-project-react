from django.test import Client, TestCase

from .models import User


class TaskURLTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    list_urls = [
        "/api/tags/",
        "/api/users/",
        "/api/recipes/",
    ]

    def test_urls(self):
        """Страница / доступна любому пользователю."""
        for url in self.list_urls:
            response = self.authorized_client.get(url)
            self.assertEqual(response.status_code, 200)
