usage: main.py [-h] [--platform {xhs,dy,ks,bili,wb,tieba,zhihu}] [--lt {qrcode,phone,cookie}] [--type {search,detail,creator}]
               [--start START] [--keywords KEYWORDS] [--get_comment GET_COMMENT] [--get_sub_comment GET_SUB_COMMENT]
               [--save_data_option {csv,db,json}] [--cookies COOKIES]

Media crawler program.

options:
  -h, --help            show this help message and exit
  --platform {xhs,dy,ks,bili,wb,tieba,zhihu}
                        Media platform select (xhs | dy | ks | bili | wb | tieba | zhihu)
  --lt {qrcode,phone,cookie}
                        Login type (qrcode | phone | cookie)
  --type {search,detail,creator}
                        crawler type (search | detail | creator)
  --start START         number of start page
  --keywords KEYWORDS   please input keywords
  --get_comment GET_COMMENT
                        whether to crawl level one comment, supported values case insensitive ('yes', 'true', 't', 'y', '1',
                        'no', 'false', 'f', 'n', '0')
  --get_sub_comment GET_SUB_COMMENT
                        'whether to crawl level two comment, supported values case insensitive ('yes', 'true', 't', 'y', '1',
                        'no', 'false', 'f', 'n', '0')
  --save_data_option {csv,db,json}
                        where to save the data (csv or db or json)
  --cookies COOKIES     cookies used for cookie login type



## 小红书搜索：
python main.py --platform xhs --lt qrcode --type search
## 小红书指定视频获取评论：
python main.py --platform xhs --lt qrcode --type detail
## 小红书创作者主页：
python main.py --platform xhs --lt qrcode --type creator

## 抖音搜索：
python main.py --platform dy --lt qrcode --type search
## 抖音指定视频获取评论：
python main.py --platform dy --lt qrcode --type detail
## 抖音创作者主页：
python main.py --platform dy --lt qrcode --type creator



