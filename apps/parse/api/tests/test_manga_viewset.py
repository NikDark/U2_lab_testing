from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.parse.models import Manga

class MangaAPIViewSetTest(APITestCase):

    list_url = reverse("manga-list")

    def set_up(self):
        self.client = APIClient()
        Manga.objects.create(title="Test manga", source="http://test_url")

    def test_get_manga_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

