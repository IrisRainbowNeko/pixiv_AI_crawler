
import time
from typing import Callable, Dict, Iterable, Optional, Tuple

import requests
from ..config import DOWNLOAD_CONFIG, NETWORK_CONFIG, OUTPUT_CONFIG
from ..utils import printInfo, printWarn, writeFailLog


def collect(args: Tuple[str, Callable, Optional[Dict]]) \
        -> Optional[Iterable[str]]:
    """[summary]
    generic metadata collector, collect metadata from templates
        e.g.: user.json, page.json, ...
        use different selector to select different elements
        args: url, selector, additional_headers
    """
    url, selector, additional_headers = args
    headers = NETWORK_CONFIG["HEADER"]
    if additional_headers is not None:
        headers.update(additional_headers)

    verbose_output = OUTPUT_CONFIG["VERBOSE"]
    error_output = OUTPUT_CONFIG["PRINT_ERROR"]
    if verbose_output:
        printInfo(f"collecting {url}")
    time.sleep(DOWNLOAD_CONFIG["THREAD_DELAY"])

    for i in range(DOWNLOAD_CONFIG["N_TIMES"]):
        try:
            response = requests.get(
                url, headers=headers,
                proxies=NETWORK_CONFIG["PROXY"],
                timeout=4)

            if response.status_code == 200:
                id_group = selector(response)
                if verbose_output:
                    printInfo(f"{url} complete")
                return id_group

        except Exception as e:
            printWarn(error_output, e)
            printWarn(error_output,
                      f"This is {i} attempt to collect {url}")

            time.sleep(DOWNLOAD_CONFIG["FAIL_DELAY"])

    printWarn(error_output, f"fail to collect {url}")
    writeFailLog(f"fail to collect {url} \n")
