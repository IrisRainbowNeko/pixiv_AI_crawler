
import concurrent.futures as futures
from typing import Iterable, Set, Tuple

from ..config import DOWNLOAD_CONFIG
from tqdm import tqdm
from ..utils import printInfo

from .download_image import downloadImage, downloadImageWithCLS


class Downloader():
    """[summary]
    download controller
    """

    def __init__(self, capacity, im_classifier=None):
        self.url_group: Set[Tuple[str, str]] = set() #[small, original]
        self.capacity = capacity
        self.im_classifier = im_classifier

    def add(self, urls: Iterable[Tuple[str, str]]):
        for url in urls:
            self.url_group.add(url)

    def download(self):
        flow_size = .0
        printInfo("===== downloader start =====")

        n_thread = DOWNLOAD_CONFIG["N_THREAD"]
        with futures.ThreadPoolExecutor(n_thread) as executor:
            with tqdm(total=len(self.url_group), desc="downloading") as pbar:
                if self.im_classifier is None:
                    exmap=executor.map(downloadImage, self.url_group)
                else:
                    exmap=executor.map(downloadImageWithCLS, self.url_group, [self.im_classifier]*len(self.url_group))
                for image_size in exmap:
                    flow_size += image_size
                    pbar.update()
                    pbar.set_description(
                        f"downloading / flow {flow_size:.2f}MB")
                    if flow_size > self.capacity:
                        executor.shutdown(wait=False, cancel_futures=True)
                        break

        printInfo("===== downloader complete =====")
        return flow_size
