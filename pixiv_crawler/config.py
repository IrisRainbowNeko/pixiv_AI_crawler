import datetime


# NOTE: MODE_CONFIG only applies to ranking crawler
MODE_CONFIG = {
    # start date
    "START_DATE": datetime.date(2022, 8, 5),
    # date range: [start, start + range - 1]
    "RANGE": 1,

    # which ranking list
    "RANKING_MODES": [
        "daily", "weekly", "monthly",
        "male", "female",
        "daily_r18", "weekly_r18",
        "male_r18", "female_r18"
    ],
    "MODE": "daily",  # choose from the above

    # illustration, manga, or both
    "CONTENT_MODES": [
        "all",  # download both illustrations & mangas
        "illust", "manga"
    ],
    "CONTENT_MODE": "illust",  # choose from the above

    # download top x in each ranking
    #   suggested x be a multiple of 50
    "N_ARTWORK": 500
}

OUTPUT_CONFIG = {
    # verbose / simplified output
    "VERBOSE": False,
    "PRINT_ERROR": False
}

NETWORK_CONFIG = {
    # proxy setting
    #   you should customize your proxy setting accordingly
    #   default is for clash
    "PROXY": {"https": "http://127.0.0.1:1080"},

    # common request header
    "HEADER": {
        #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1",
    }
}

USER_CONFIG = {
    # user id
    #   access your pixiv user profile to find this
    #   e.g. https://www.pixiv.net/users/xxxx
    "USER_ID": "",

    "COOKIE": ""
}


DOWNLOAD_CONFIG = {
    # image save path
    #   NOTE: DO NOT miss "/"
    "STORE_PATH": "images_85/",

    # abort request / download
    #   after 10 unsuccessful attempts
    "N_TIMES": 10,

    # need tag ?
    "WITH_TAG": True,

    # waiting time (s) after failure
    "FAIL_DELAY": 1,

    # max parallel thread number
    "N_THREAD": 12,
    # waiting time (s) after thread start
    "THREAD_DELAY": 1,
}
