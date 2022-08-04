import datetime


# NOTE: MODE_CONFIG only applies to ranking crawler
MODE_CONFIG = {
    # start date
    "START_DATE": datetime.date(2022, 6, 10),
    # date range: [start, start + domain - 1]
    "RANGE": 1,

    # which ranking list
    "RANKING_MODES": [
        "daily", "weekly", "monthly",
        "male", "female",
        "daily_r18", "weekly_r18",
        "male_r18", "female_r18"
    ],
    "MODE": "daily",  # choose from the above

    "EXP_TAGS": ['漫画'],  # choose from the above

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
    "PROXY": {"https": "127.0.0.1:1080"},

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
    "USER_ID": "15795946",

    "COOKIE": "first_visit_datetime_pc=2022-01-24+16%3A01%3A41; p_ab_id=9; p_ab_id_2=8; p_ab_d_id=1498797893; yuid_b=FhkhVFg; c_type=22; privacy_policy_notification=0; a_type=0; b_type=1; PHPSESSID=15795946_96FmWeSMrbdTxszmUCYVkGQtnpTSfRen; device_token=985ffc8cc3d59bb88f39be265f1ccb24; _fbp=fb.1.1658305800937.819174754; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.51999291.1659070859; login_ever=yes; _gcl_au=1.1.1740323667.1659070883; tag_view_ranking=VPl-5u9cu6~_EOd7bsGyl~1TeQXqAyHD~h4LK2feuuI~Lt-oEicbBr~ziiAzr_h04~0xRZYD1xTs~aKhT3n4RHZ~0xsDLqCEW6~ETjPkL0e6r~RTJMXD26Ak~wV16kRYtRD~LX3_ayvQX4~MnGbHeuS94~TqiZfKmSCg~i6xpz1p4ti~_Cu_8HMURl~ZQngJx8lsH~D5OM6xov0K~Py9ClaXrat~2fXUw8vALl~mqjSGT7T6W~3gc3uGrU1V~-98s6o2-Rp~EZQqoW9r8g~43DoAn1Cyu~eBgm93roen~HieBiosxBn~T40wdiG5yy~BN7FnIP06x~w8ffkPoJ_S~zyKU3Q5L4C~j3leh4reoN~eK9vnMvjjT~gpglyfLkWs~ITqZ5UzdOC~ryeW-BDpTM~HT4d9_1J8X~pzZvureUki~fTfFgPnDb6~CdRA5IfUV3~qrSxJbykR_~qejSKUWDJ4~BC84tpS1K_~QIc0RHSvtN~QaiOjmwQnI~qXn3w4VVkw~oaVGtg6mpV~D0nMcn6oGk~HY55MqmzzQ~N0yI5Cxu-1~eVxus64GZU~pnCQRVigpy~cD2FJpAxIO~0rsCr94LAC~W37z3m4gNa~nInT2dTMR6~yOqOtdektt~WD2JDye622~gnmsbf1SSR; _ga=GA1.1.994638256.1658305786; __cf_bm=gfybVNHUBr0p1RJTYrbky2NZ77h82MbFe8CY3M1fAwE-1659076138-0-AeUXmCfncZFF3qvw3P1U4DZ/uuFRWRhAMR3It4XN5P+kIYmslyWdq3QpxG72l2iYgLF9lgj2M2jwMEt+w+cFncoiHViJIghyW9ST7/aSz1H8ATxah8TSisnwjweFxfxr3yANYFGLku/LzxS+maoVRiwnBqqxh7kCaev1fL9HCB7kBQVEHBs/Q6XlpN5FvlEhcA==; privacy_policy_agreement=5; _ga_75BBYNYN9J=GS1.1.1659074983.3.1.1659076210.0"
}


DOWNLOAD_CONFIG = {
    # image save path
    #   NOTE: DO NOT miss "/"
    "STORE_PATH": "images_610/",

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
