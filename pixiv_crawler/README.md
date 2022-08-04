
[TOC]

## 杂项

### 部分开发记录

- Notations

  - `artwork_id`: "63120410"

  - `artwork_url`: https://www.pixiv.net/artworks/93172108

    每个`artwork`可能包含多张图片

  - `image_url`: "https://i.pximg.net/img-original/img/2021/10/02/18/47/29/93172108_p1.jpg"

- 在`image_mix`中加入了`BVH Tree`来加速3D最近点的查询

- 将从`json/html`收集`artwork`的模块整集成到了`collect_unit.py`

  通过传入不同的`selector`来筛选不同的数据

- 移除了对下载数量的精准计算

  以排行榜为例，单个`json`文件包含50幅作品，只能保证下载数量为$\lceil \frac{x}{50} \rceil\times 50$

- 添加了标签`selectTag()`

  启用`WITH_TAG`后会生成`tags.json`记录每张作品的标签

- 添加了关键词下载，默认行为为按热度排序（需要高级账户，否则为默认排序）



### 主要模块

```
pixiv_crawler
│   config.py
│   main.py
│   README.md
│   utils.py
│
├───collector
│   │   collector.py
│   │   collector_unit.py
│   └───selectors.py
│
├───crawlers
│   │   bookmark_crawler.py
│   │   keyword_crawler.py
│   │   ranking_crawler.py
│   └───users_crawler.py
│
└───downloader
    │   downloader.py
    └───download_image.py
```

- `config.py`: 配置文件

- `main.py`: 主程序

- `utils.py`: 辅助函数

- `collector/`

  - `collector.py`: 使用`collector_unit`

  - `collector_unit.py`: 收集 `artwork_url`, `image_url`等数据

    通过传入不同的`selector`来筛选不同的数据

  - `selectors.py`: 从`json/html`中收集不同数据的函数库

- `crawlers/`

  爬虫入口，收集`artwork_id`数据

  - `bookmark_crawler.py`
  - `keyword_crawler.py`
  - `ranking_crawler.py`
  - `users_crawler.py`

- `downloader/`

  - `downloader.py`: 使用`download_image`
  - `download_image.py`: 根据`image_url`下载图片



### 附录

- `pixiv.net/robots.txt`

```
User-agent: *
Disallow: /rpc/index.php?mode=profile_module_illusts&user_id=*&illust_id=*
Disallow: /ajax/illust/*/recommend/init
Disallow: *return_to*
Disallow: /?return_to=
Disallow: /login.php?return_to=
Disallow: /index.php?return_to=

//搜索功能
Disallow: /tags/* * *
Disallow: /tags/*%20*%20*

Disallow: /users/*/followers
Disallow: /users/*/mypixiv
//别人的关注
Disallow: /users/*/bookmarks
Disallow: /novel/comments.php?id=


Disallow: /en/group

Disallow: /en/tags/* * *
Disallow: /en/tags/*%20*%20*

Disallow: /en/search/

Disallow: /en/users/*/followers
Disallow: /en/users/*/mypixiv
Disallow: /en/users/*/bookmarks
Disallow: /en/novel/comments.php?id=

Disallow: /fanbox/search
Disallow: /fanbox/tag
```

