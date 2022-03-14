from rest_framework.test import APITestCase
import json


class TestMangaEndPoint(APITestCase):
      
    def test_get_api_manga_status_code_equals_400(self):
        response = self.client.get('http://127.0.0.1:8000/api/manga/')
        self.assertEqual(response.status_code, 400)

    def test_get_api_manga_response_content_equals_error(self):
        response = self.client.get('http://127.0.0.1:8000/api/manga/')
        self.assertEqual(json.loads(response.content),  {"error": "No title found"})

    def test_get_api_manga_id_965_response_not_equals_empty(self):
        response = self.client.get('http://127.0.0.1:8000/api/manga/965')
        self.assertNotEqual(response.content,{})

# chepter with title Hello for manga герцогиня на чердаке # 968 was created earlier 
    def test_get_api_manga_with_chepterid_968_not_equals_empty(self):
        response = self.client.get('http://127.0.0.1:8000/api/manga/968/chapters')
        self.assertNotEqual(response.content,{})

    def test_get_api_manga_177_images_status_code_equals_404(self):
        response = self.client.get('http://127.0.0.1:8000/api/manga/177/images')
        self.assertEqual(response.status_code, 404)
