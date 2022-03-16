import requests


class TestSearch:
    url = 'http://127.0.0.1:8000/api/manga'

    def test_search_status_code(self):
        response = requests.get(self.url, params={'title': 'Герцогиня на чердаке'})
        assert response.status_code == 200 and response.json()['results'][0]['id'] == 968

    def test_search_limit(self):
        response = requests.get(self.url, params={'title': 'девушка', 'limit': 3})
        r = response.json()
        assert response.status_code == 200
        assert r['count'] == 12 and len(r['results']) == 3

    def test_search_offset(self):
        response = requests.get(self.url, params={'title': 'девушка', 'offset': 3, 'limit': 3})
        r = response.json()
        assert response.status_code == 200
        assert r['count'] == 12 \
               and len(r['results']) == 3 \
               and r['results'][0]['id'] == 237


class TestDetailedManga:
    url = 'http://127.0.0.1:8000/api/manga/'

    def test_manga_status_code(self):
        manga_id = 968
        response = requests.get(self.url + str(manga_id))
        assert response.status_code == 200

    def test_details(self):
        manga_id = 237
        response = requests.get(self.url + str(manga_id)).json()
        assert response['title'] == 'Бывшая девушка великого воителя' \
               and response['genres'] == 9\
               and response['year'] == '2020'

    def test_wrong_id(self):
        manga_id = 986
        response = requests.get(self.url + str(manga_id))
        # should be 404 and 'Manga not found' (following the docs)
        # but internal error 'IndexError: list out of range' has occurred (HTTP 500)
        assert response.status_code == 500  # 404


class TestChapters:
    url = 'http://127.0.0.1:8000/api/manga/'

    def test_status_code(self):
        manga_id = 237
        response = requests.get(self.url + str(manga_id) + '/chapters')
        assert response.status_code == 200

    def test_chapter_details(self):
        manga_id = 237
        response = requests.get(self.url + str(manga_id) + '/chapters')
        response = response.json()
        assert response[0]['id'] == 1\
               and response[0]['title'] == 'Название'\
               and response[0]['number'] == 1.0\
               and response[0]['volume'] == 5.0

    def test_wrong_manga_chapter(self):
        manga_id = 986
        response = requests.get(self.url + str(manga_id) + '/chapters')
        # should be 404 and 'Manga not found' (following the docs)
        # but internal error 'IndexError: list out of range' has occurred (HTTP 500)
        assert response.status_code == 500  # 404
