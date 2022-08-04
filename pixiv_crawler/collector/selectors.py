import json
import re
from typing import List, Set, Tuple

from pyquery import PyQuery
from requests.models import Response
from ..utils import printError, writeFailLog


def selectTag(response: Response) -> List[str]:
    """[summary]
    url: https://www.pixiv.net/artworks/xxxxxx
    collect all image tags from (artwork.html)

    Returns:
        List[str]: tags
    """
    result = re.search("artworks/(\d+)", response.url)
    printError(result is None, "bad response in selectTag")
    illust_id = result.group(1)
    content = json.loads(
        PyQuery(response.text).find(
            "#meta-preload-data").attr("content"))
    return [
        tag["translation"]["en"] if "translation" in tag else tag["tag"]
        for tag in content["illust"][illust_id]["tags"]["tags"]
    ]


def selectPage(response: Response) -> Set[Tuple[str, str]]:
    """[summary]
    url: https://www.pixiv.net/ajax/illust/xxxx/pages?lang=zh
    collect all image urls from (page.json)

    Returns:
        Set[str]: urls
    """
    group = set()
    for url in response.json()["body"]:
        group.add((url["urls"]["small"], url["urls"]["original"]))
    return group


def selectRanking(response: Response) -> Set[str]:
    """[summary]
    url: https://www.pixiv.net/ranking.php?mode=daily&date=20200801&p=1&format=json
    collect all illust_id (image_id) from (ranking.json)

    Returns:
        Set[str]: illust_id (image_id)
    """
    image_ids = [artwork["illust_id"]
                 for artwork in response.json()["contents"]]
    return set(map(str, image_ids))


def selectUser(response: Response) -> Set[str]:
    """[summary]
    url: https://www.pixiv.net/ajax/user/23945843/profile/all?lang=zh
    collect all illust_id (image_id) from (user.json)

    Returns:
        Set[str]: illust_id (image_id)
    """
    return set(response.json()["body"]["illusts"].keys())


def selectBookmark(response: Response) -> Set[str]:
    """[summary]
    url: https://www.pixiv.net/ajax/user/xxx/illusts/bookmarks?tag=&offset=0&limit=48&rest=show&lang=zh
    collect all illust_id (image_id) from (bookmark.json)

    Returns:
        Set[str]: illust_id (image_id)
    """
    # NOTE: id of disable artwork is int (not str)
    id_group: Set[str] = set()
    for artwork in response.json()["body"]["works"]:
        illust_id = artwork["id"]
        if isinstance(illust_id, str):
            id_group.add(artwork["id"])
        else:
            writeFailLog(f"disable artwork {illust_id} \n")
    return id_group


def selectKeyword(response: Response) -> Set[str]:
    """[summary]
    url: https://www.pixiv.net/ajax/search/artworks/{xxxxx}?word={xxxxx}&order=popular_d&mode=all&p=1&s_mode=s_tag_full&type=all&lang=zh"
    collect all illust_id (image_id) from (keyword.json)

    Returns:
        Set[str]: illust_id (image_id)
    """
    # NOTE: id of disable artwork is int (not str)
    id_group: Set[str] = set()
    for artwork in response.json()[
            "body"]["illustManga"]["data"]:
        id_group.add(artwork["id"])
    return id_group
