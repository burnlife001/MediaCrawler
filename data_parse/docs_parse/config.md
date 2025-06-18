## Answer

抖音爬虫的三种模式需要设置不同的配置参数，每种模式针对不同的数据获取场景。

### 搜索模式 (search)
```bash
python main.py --platform dy --lt qrcode --type search
```

**必需配置参数：**
- `KEYWORDS` - 搜索关键词，多个关键词用逗号分隔  
- `CRAWLER_MAX_NOTES_COUNT` - 每个关键词最大爬取视频数量

**工作流程：** 程序会根据关键词搜索视频  ，然后保存视频信息  ，最后获取评论  

### 指定视频模式 (detail)
```bash
python main.py --platform dy --lt qrcode --type detail
```

**必需配置参数：**
- `DY_SPECIFIED_ID_LIST` - 指定要爬取的视频ID列表  

**工作流程：** 程序会直接获取指定ID的视频详情  ，并发获取视频信息后获取评论  

### 创作者主页模式 (creator)
```bash
python main.py --platform dy --lt qrcode --type creator
```

**必需配置参数：**
- `DY_CREATOR_ID_LIST` - 创作者ID列表(sec_uid)  

**工作流程：** 程序会获取创作者信息和所有视频  ，通过API获取用户信息  ，然后获取所有视频  

### 通用配置参数

所有模式都支持的参数：
- `ENABLE_GET_COMMENTS` - 是否获取评论  
- `ENABLE_GET_SUB_COMMENTS` - 是否获取二级评论  
- `CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES` - 单个视频最大评论数  

## Notes

三种模式的核心区别在于数据来源：search模式通过关键词搜索获取视频，detail模式直接获取指定ID的视频，creator模式获取特定创作者的所有视频。每种模式都会最终调用相同的评论获取逻辑，但数据获取的起点不同。

