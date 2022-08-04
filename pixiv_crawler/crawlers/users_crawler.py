from ..collector.collector import Collector
from ..collector.collector_unit import collect
from ..collector.selectors import selectUser
from ..config import USER_CONFIG
from ..downloader.downloader import Downloader
from ..utils import printInfo


class UserCrawler():
    """[summary]
    collect all artworks from single artist

    NOTE: url sample: "https://www.pixiv.net/ajax/user/23945843/profile/all?lang=zh"
    """

    def __init__(self, artist_id, capacity=1024):
        self.artist_id = artist_id

        self.downloader = Downloader(capacity)
        self.collector = Collector(self.downloader)

    def collect(self):
        url = f"https://www.pixiv.net/ajax/user/{self.artist_id}/profile/all?lang=zh"
        additional_headers = {
            "x-user-id": USER_CONFIG["USER_ID"],
            "Referer": f"https://www.pixiv.net/users/{self.artist_id}/illustrations"
        }
        image_ids = collect(
            (url, selectUser, additional_headers))
        if image_ids is not None:
            self.collector.add(image_ids)
        printInfo(f"===== collect user {self.artist_id} complete =====")

    def run(self):
        self.collect()
        self.collector.collect()
        return self.downloader.download()
