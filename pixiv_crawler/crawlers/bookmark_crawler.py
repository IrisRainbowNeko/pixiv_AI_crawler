import concurrent.futures as futures
import time
from typing import Set

import requests
from ..collector.collector import Collector
from ..collector.collector_unit import collect
from ..collector.selectors import selectBookmark
from ..config import DOWNLOAD_CONFIG, NETWORK_CONFIG, OUTPUT_CONFIG, USER_CONFIG
from ..downloader.downloader import Downloader
from tqdm import tqdm
from ..utils import printError, printInfo, printWarn


class BookmarkCrawler():
    """[summary]
    download user's public bookmarks
    """

    def __init__(self, n_images=200, capacity=1024):
        self.n_images = n_images
        self.uid = USER_CONFIG["USER_ID"]
        self.url = f"https://www.pixiv.net/ajax/user/{self.uid}/illusts"

        self.downloader = Downloader(capacity)
        self.collector = Collector(self.downloader)

    def __requestCount(self):
        """[summary]
        get count-badge
        url sample: "https://www.pixiv.net/ajax/user/xxxx/illusts/bookmark/tags?lang=zh"
        """

        url = self.url + "/bookmark/tags?lang=zh"
        printInfo("===== requesting bookmark count =====")

        headers = {"COOKIE": USER_CONFIG["COOKIE"]}
        headers.update(NETWORK_CONFIG["HEADER"])
        error_output = OUTPUT_CONFIG["PRINT_ERROR"]
        for i in range(DOWNLOAD_CONFIG["N_TIMES"]):
            try:
                response = requests.get(
                    url, headers=headers,
                    proxies=NETWORK_CONFIG["PROXY"],
                    timeout=4)

                if response.status_code == 200:
                    n_total = int(response.json()["body"]["public"][0]["cnt"])
                    self.n_images = min(self.n_images, n_total)
                    printInfo(f"select {self.n_images}/{n_total} artworks")
                    printInfo("===== request bookmark count complete =====")
                    return

            except Exception as e:
                printWarn(error_output, e)
                printWarn(error_output,
                          f"This is {i} attempt to request bookmark count")

                time.sleep(DOWNLOAD_CONFIG["FAIL_DELAY"])

        printWarn(True, "check COOKIE config")
        printError(True, "===== fail to get bookmark count =====")

    def collect(self):
        """[summary]
        collect illust_id from bookmark
        url sample: "https://www.pixiv.net/ajax/user/xxx/illusts/bookmarks?
            tag=&offset=0&limit=48&rest=show&lang=zh"
        NOTE: [offset + 1, offset + limit]
        NOTE: id of disable artwork is int (not str)
        """

        # NOTE: default block_size is 48
        ARTWORK_PER = 48
        n_page = (self.n_images - 1) // ARTWORK_PER + 1  # ceil
        printInfo(f"===== start collecting {self.uid}'s bookmarks =====")

        urls: Set[str] = set()
        for i in range(n_page):
            urls.add(self.url + "/bookmarks?tag=&" +
                     f"offset={i * ARTWORK_PER}&limit={ARTWORK_PER}&rest=show&lang=zh")

        n_thread = DOWNLOAD_CONFIG["N_THREAD"]
        with futures.ThreadPoolExecutor(n_thread) as executor:
            with tqdm(total=len(urls), desc="collecting ids") as pbar:
                additional_headers = {"COOKIE": USER_CONFIG["COOKIE"]}
                for image_ids in executor.map(collect, zip(
                        urls, [selectBookmark] * len(urls),
                        [additional_headers] * len(urls))):
                    if image_ids is not None:
                        self.collector.add(image_ids)
                    pbar.update()

        printInfo("===== collect bookmark complete =====")
        printInfo(f"downloadable artworks: {len(self.collector.id_group)}")

    def run(self):
        self.__requestCount()
        self.collect()
        self.collector.collect()
        return self.downloader.download()
