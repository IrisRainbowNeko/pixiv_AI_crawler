import concurrent.futures as futures
from typing import Set

from ..collector.collector import Collector
from ..collector.collector_unit import collect
from ..collector.selectors import selectKeyword
from ..config import DOWNLOAD_CONFIG, USER_CONFIG
from ..downloader.downloader import Downloader
from tqdm import tqdm
from ..utils import printInfo


class KeywordCrawler():
    """[summary]
    download search results of a keyword (sorted by popularity)
    """

    def __init__(self, keyword: str, mode: str = "safe", n_images=200, capacity=1024, im_classifier=None):
        assert mode in ["safe", "r18", "all"]

        self.keyword = keyword
        self.mode = mode
        self.n_images = n_images

        self.downloader = Downloader(capacity, im_classifier)
        self.collector = Collector(self.downloader)

    def collect(self):
        """[summary]
        collect illust_id from keyword result
        url sample: "https://www.pixiv.net/ajax/search/artworks/{xxxxx}?
            word={xxxxx}&order=popular_d&mode=all&p=1&s_mode=s_tag_full&type=all&lang=zh"
        """

        # each keyword.json contains 60 artworks
        ARTWORK_PER = 60
        n_page = (self.n_images - 1) // ARTWORK_PER + 1  # ceil
        printInfo(f"===== start collecting {self.keyword} =====")

        urls: Set[str] = set()
        url = "https://www.pixiv.net/ajax/search/artworks/{}?" + \
              "word={}&order=popular_d" + f"&mode={self.mode}" + \
              "&p={}&s_mode=s_tag_full&type=all&lang=zh"
        for i in range(n_page):
            urls.add(url.format(self.keyword, self.keyword, i + 1))

        n_thread = DOWNLOAD_CONFIG["N_THREAD"]
        with futures.ThreadPoolExecutor(n_thread) as executor:
            with tqdm(total=len(urls), desc="collecting ids") as pbar:
                additional_headers = {"COOKIE": USER_CONFIG["COOKIE"]}
                for image_ids in executor.map(collect, zip(
                        urls, [selectKeyword] * len(urls),
                        [additional_headers] * len(urls))):
                    if image_ids is not None:
                        self.collector.add(image_ids)
                    pbar.update()

        printInfo(f"===== collect {self.keyword} complete =====")

    def run(self):
        self.collect()
        self.collector.collect()
        return self.downloader.download()
