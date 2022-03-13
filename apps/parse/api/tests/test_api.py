import datetime
import decimal

import pytz
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.parse.api.serializers import MANGA_FIELDS, CHAPTER_FIELDS
from apps.parse.api.tests import resources
from apps.parse.models import Manga, Chapter


class APIMangaListTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.endpoint_url = reverse("manga-list")

        for manga_index in range(1, 6):
            Manga.objects.create(title=f"Manga {manga_index}", source_url=f"https://test_manga_index_{manga_index}")

    def test_manga_list__empty_query_path(self):
        response = self.client.get(self.endpoint_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), resources.TITLE_NOT_FOUND_ERR)

    def test_manga_list__filtering_without_title_param(self):
        response = self.client.get(self.endpoint_url, {"title": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), resources.TITLE_NOT_FOUND_ERR)

    def test_manga_list__not_exist_manga(self):
        manga, _ = Manga.objects.get_or_create(title="Not Exist Manga Title")
        manga.delete()
        response = self.client.get(self.endpoint_url, {"title": "Not Exist Manga Title"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), resources.SEARCH_TITLE_IS_NOT_EXIST)

    def test_manga_list_exist_manga(self):
        manga, _ = Manga.objects.get_or_create(title="Exist Manga Title")
        response = self.client.get(self.endpoint_url, {"title": "Exist Manga Title"})
        serialized_data = Manga.objects.filter(pk=manga.id).parse_values(*MANGA_FIELDS)

        self.assertEqual(response.json()["results"], serialized_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manga_list_filtering_count(self):

        Manga.objects.create(title='Test title')

        response = self.client.get(self.endpoint_url, {"title": "Manga"})
        test_response = self.client.get(self.endpoint_url, {"title": "Test"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 5)
        self.assertEqual(len(test_response.json()["results"]), 1)

    def test_manga_list_filtering_count_limit(self):
        response = self.client.get(self.endpoint_url, {"title": "Manga", "limit": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 2)

    def test_manga_list_filtering_offset_limit(self):
        response = self.client.get(self.endpoint_url, {"title": "Manga", "limit": 1, "offset": 4})

        except_result_manga = Manga.objects.filter(title__icontains="Manga").parse_values(*MANGA_FIELDS)[4]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"], [except_result_manga])


class APIRetrieveTestCase(APITestCase):

    def test_api_manga_exist_without_updated_detail(self):
        manga = Manga.objects.create(title="Manga #1")
        endpoint_url = reverse("manga-detail", kwargs={"pk": manga.pk})
        response = self.client.get(endpoint_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), resources.MANGA_IS_UPDATED)

    def test_api_manga_updated_detail(self):
        timezone = pytz.timezone("Europe/Minsk")
        manga = Manga.objects.create(title="Manga #1", updated_detail=datetime.datetime.now(tz=timezone))

        endpoint_url = reverse("manga-detail", kwargs={"pk": manga.pk})
        serialized_data = Manga.objects.filter(pk=manga.pk).parse_values(*MANGA_FIELDS)[0]

        response = self.client.get(endpoint_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.json(), resources.MANGA_IS_UPDATED)
        self.assertEqual(response.json(), serialized_data)

    def test_api_manga_index_out_range(self):
        endpoint_url = reverse("manga-detail", kwargs={"pk": 1})

        with self.assertRaises(IndexError) as context:
            self.client.get(endpoint_url)

        self.assertTrue("list index out of range" in str(context.exception))

    def test_api_chapters(self):
        timezone = pytz.timezone("Europe/Minsk")
        manga = Manga.objects.create(
            title="Магическая битва",
            alt_title="Jujutsu kaisen",
            rating=decimal.Decimal("4.2"),
            thumbnail="https://images-na.ssl-images-amazon.com/images/I/81KHmMZIZhL.jpg",
            description="Test description",
            source_url="https://readmanga.io/magicheskaia_bitva",
            year="2018",
            updated_detail=datetime.datetime.now(tz=timezone)
        )
        Chapter.objects.create(
            manga=manga,
            title="Магическая битва(Юта Окотцу)",
            link="https://readmanga.io/blich__A5327/",
            number=0,
            volume=0
        )
        Chapter.objects.create(
            manga=manga,
            title="Магическая битва(Сукуна)",
            link="https://readmanga.io/blich__A5327/",
            number=2,
            volume=1
        )

        endpoint_url = reverse("manga-chapters-list", kwargs={"pk": manga.pk})
        response = self.client.get(endpoint_url)

        chapters = list(manga.chapters.order_by("-volume", "-number").values(*CHAPTER_FIELDS))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), chapters)

    def test_api_empty_chapters(self):
        timezone = pytz.timezone("Europe/Minsk")
        manga = Manga.objects.create(
            title="Магическая битва",
            alt_title="Jujutsu kaisen",
            rating=decimal.Decimal("4.2"),
            thumbnail="https://images-na.ssl-images-amazon.com/images/I/81KHmMZIZhL.jpg",
            description="Test description",
            source_url="https://readmanga.io/magicheskaia_bitva",
            year="2018",
            updated_detail=datetime.datetime.now(tz=timezone)
        )

        endpoint_url = reverse("manga-chapters-list", kwargs={"pk": manga.pk})
        response = self.client.get(endpoint_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])
