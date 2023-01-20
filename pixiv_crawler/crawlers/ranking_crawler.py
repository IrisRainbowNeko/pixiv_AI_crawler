import concurrent.futures as futures
import datetime
import re
from typing import Set

from ..collector.collector import Collector
from ..collector.collector_unit import collect
from ..collector.selectors import selectRanking
from ..config import DOWNLOAD_CONFIG, MODE_CONFIG, USER_CONFIG
from ..downloader.downloader import Downloader
from tqdm import tqdm
from ..utils import printInfo


class RankingCrawler():
    def __init__(self, capacity=1024, im_classifier=None):
        """[summary]
        download artworks from ranking

        Args:
            capacity (int, optional): flow capacity (MB)
        """
        self.date = MODE_CONFIG["START_DATE"]
        self.range = MODE_CONFIG["RANGE"]
        self.mode = MODE_CONFIG["MODE"]
        self.content = MODE_CONFIG["CONTENT_MODE"]

        # NOTE:
        #   1. url sample: "https://www.pixiv.net/ranking.php?
        #       mode=daily&date=20200801&p=1&format=json"
        #   2. ref url sample: "https://www.pixiv.net/ranking.php?mode=daily&date=20200801"
        self.url = "https://www.pixiv.net/ranking.php?" + \
            f"mode={self.mode}&content={self.content}" + \
            "&date={}&p={}&format=json"

        self.downloader = Downloader(capacity, im_classifier)
        self.collector = Collector(self.downloader)

    def __collect(self):
        """[summary]
        collect illust_id from ranking
        """
        # each ranking.json contains 50 artworks
        ARTWORK_PER = 50
        n_page = (MODE_CONFIG["N_ARTWORK"] - 1) // ARTWORK_PER + 1  # ceil

        def addData(current: datetime.date, days):
            return current + datetime.timedelta(days)

        printInfo(f"===== start collecting {self.mode}:{self.content} ranking =====")
        printInfo("from {} to {}".format(
            self.date.strftime("%Y-%m-%d"),
            addData(self.date, self.range - 1).strftime("%Y-%m-%d")))

        urls: Set[str] = set()
        for _ in range(self.range):
            for i in range(n_page):
                urls.add(self.url.format(
                    self.date.strftime("%Y%m%d"), i + 1))
            self.date = addData(self.date, 1)

        n_thread = DOWNLOAD_CONFIG["N_THREAD"]
        with futures.ThreadPoolExecutor(n_thread) as executor:
            with tqdm(total=len(urls), desc="collecting ids") as pbar:
                additional_headers = [
                    {
                        "Referer": re.search("(.*)&p", url).group(1),
                        "x-requested-with": "XMLHttpRequest",
                        "COOKIE": USER_CONFIG["COOKIE"]
                    }
                    for url in urls]
                for image_ids in executor.map(collect, zip(
                        urls, [selectRanking] * len(urls), additional_headers)):
                    if image_ids is not None:
                        self.collector.add(image_ids)
                    pbar.update()

        printInfo(f"===== collect {self.mode} ranking complete =====")

    def run(self) -> float:
        self.__collect()
        self.collector.collect()
        return self.downloader.download()
