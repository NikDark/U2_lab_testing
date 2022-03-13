from django.test import TestCase
from django.urls import reverse
from apps.parse.models import Manga


class PostModelTest(TestCase):

    def setUp(self):
        Manga.objects.create(title='19 дней — Однажды')

    def test_text_content(self):
        post = Manga.objects.get(title='19 дней — Однажды')
        expected_object_name = f'{post.text}'
        self.assertEqual(expected_object_name, 'just a test')

    def test_view_url_by_name(self):
        resp = self.client.get(reverse('manga'))
        self.assertEqual(resp.status_code, 200)
