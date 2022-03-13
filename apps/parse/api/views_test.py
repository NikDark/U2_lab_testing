import requests
from jsonschema import validate
from apps.parse.api.schemas import API_MANGA_ID, API_MANGA_ID_CHAPTERS, API_MANGA, Resp
params_api_manga = {
        'title': "Manga title",
        'limit': "Query limit",
        'offset': "Query offset"
    }
params_api_manga_id = {
        'mangaId': "ID of manga to return",
    }
params_api_manga_id_chapters = {
        'mangaId': "ID of manga to get chapters for",
    }
params_api_manga_chapter_images = {
        'chapterId': "D of chapter to get images for",
        'parse': 'Whether to run parsing of images again (if links are broken)',
}


def test_api_manga():
    r = requests.get("http://127.0.0.1:8000/api/manga/", params=params_api_manga)
    response = Resp(r)
    response.assert_status_code(200).assert_headers('application/json')
    response_body = r.json()
    for i in response_body:
        validate(i, API_MANGA)


def test_api_manga_id():
    for i in range(1, 10):
        r = requests.get(f"http://127.0.0.1:8000/api/manga/{i}", params=params_api_manga_id)
        response = Resp(r)
        response.assert_status_code(200).assert_headers('application/json')
        response_body = r.json()
        validate(response_body, API_MANGA_ID)


def test_api_manga_id_chapters():
    for i in range(1, 10):
        r = requests.get(f"http://127.0.0.1:8000/api/manga/{i}/chapters", params=params_api_manga_id_chapters)
        response = Resp(r)
        response.assert_status_code(200).assert_headers('application/json')
        response_body = r.json()
        for j in response_body:
            validate(j, API_MANGA_ID_CHAPTERS)


def test_api_manga_chapter_images():
    for i in range(1, 10):
        r = requests.get(f"http://127.0.0.1:8000/api/manga/{i}/chapters", params=params_api_manga_chapter_images)
        response = Resp(r)
        response.assert_status_code(200).assert_headers('application/json')
        response_body = r.json()
        assert response_body is not None
