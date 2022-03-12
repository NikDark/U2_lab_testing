import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manga_reader.settings")
import unittest
from .views import MangaViewSet


if __name__ == '__main__':
    unittest.main()
