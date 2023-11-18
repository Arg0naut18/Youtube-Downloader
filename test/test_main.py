import unittest
from src.main import YTDownloader


class TestYTDownloader(unittest.TestCase):
    def test_start_download(self):
        app = YTDownloader()
        app()