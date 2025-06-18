#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫控制器
"""

import asyncio
import sys
import os
import json
import random
import re
from typing import Dict, Any, Callable, Optional, List
import logging
from pathlib import Path

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

# 添加必要的变量
playwright_instance = None


class CrawlerController:
    """爬虫控制器类"""

    def __init__(self, platform: str, config: Dict[str, Any],
                 progress_callback: Optional[Callable] = None,
                 data_callback: Optional[Callable] = None):
        self.platform = platform
        self.config = config
        self.progress_callback = progress_callback
        self.data_callback = data_callback

        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.should_stop = False

        # 爬虫实例
        self.crawler = None
        self.browser_context = None
        self.context_page = None

        # 数据统计
        self.total_comments = 0
        self.crawled_comments = 0
        self.current_aweme_id = None

        # 数据存储
        self.comments_data = []
        self.content_data = []
    
    async def crawl_by_url(self, url: str):
        """根据URL爬取数据"""
        try:
            self.is_running = True
            self.should_stop = False
            self.comments_data.clear()
            self.content_data.clear()

            # 解析URL获取ID
            from ui.controllers.url_parser import URLParser
            parser = URLParser()
            parsed_result = parser.parse_url(url, self.platform)

            if not parsed_result:
                raise Exception("无法解析URL")

            # 更新进度
            self._update_progress({
                "status": "初始化爬虫...",
                "percentage": 0,
                "crawled": 0,
                "total": 0
            })

            # 应用配置到MediaCrawler
            await self._setup_config(url, parsed_result)

            # 更新进度
            self._update_progress({
                "status": "启动浏览器...",
                "percentage": 10,
                "crawled": 0,
                "total": 0
            })

            # 创建爬虫实例
            await self._create_crawler()

            if self.should_stop:
                return

            # 更新进度
            self._update_progress({
                "status": "初始化浏览器环境...",
                "percentage": 20,
                "crawled": 0,
                "total": 0
            })

            # 初始化浏览器环境
            await self._init_browser_environment()

            if self.should_stop:
                return

            # 更新进度
            self._update_progress({
                "status": "检查登录状态...",
                "percentage": 30,
                "crawled": 0,
                "total": 0
            })

            # 处理登录
            await self._handle_login()

            if self.should_stop:
                return

            # 更新进度
            self._update_progress({
                "status": "开始爬取视频信息...",
                "percentage": 40,
                "crawled": 0,
                "total": 1
            })

            # 执行爬取
            await self._execute_crawling(parsed_result)

            # 完成
            if not self.should_stop:
                self._update_progress({
                    "status": "爬取完成",
                    "percentage": 100,
                    "crawled": self.crawled_comments,
                    "total": max(self.total_comments, self.crawled_comments)
                })

        except Exception as e:
            self.logger.error(f"爬取失败: {str(e)}")
            self._update_progress({
                "status": f"爬取失败: {str(e)}",
                "percentage": 0,
                "crawled": 0,
                "total": 0
            })
            raise
        finally:
            await self._cleanup()
            self.is_running = False
    
    async def _setup_config(self, url: str, parsed_result: Dict[str, Any]):
        """设置配置"""
        try:
            from ui.utils.config_manager import ConfigManager
            config_manager = ConfigManager()

            # 应用UI配置到MediaCrawler
            config_manager.apply_to_mediacrawler(self.config)

            # 导入配置模块
            import config.base_config as base_config

            # 设置特定URL的配置
            if self.platform == "dy":
                video_id = parsed_result.get("id")
                if video_id and video_id not in ["unknown", "short_link"]:
                    # 有明确的视频ID
                    base_config.DY_SPECIFIED_ID_LIST = [video_id]
                    self.current_aweme_id = video_id
                else:
                    # 短链接或无法解析的链接，使用URL直接访问
                    base_config.DY_SPECIFIED_ID_LIST = []
                    # 存储URL用于后续处理
                    self.target_url = url

            elif self.platform == "xhs":
                base_config.XHS_SPECIFIED_NOTE_URL_LIST = [url]

            # 设置爬取类型为详情模式
            base_config.CRAWLER_TYPE = "detail"

            self.logger.info(f"配置设置完成: {self.platform}, URL: {url}")

        except Exception as e:
            self.logger.error(f"设置配置失败: {str(e)}")
            raise

    async def _create_crawler(self):
        """创建爬虫实例"""
        try:
            # 导入爬虫工厂
            from main import CrawlerFactory

            # 创建爬虫实例
            self.crawler = CrawlerFactory.create_crawler(self.platform)
            self.logger.info(f"爬虫实例创建成功: {self.platform}")

        except Exception as e:
            self.logger.error(f"创建爬虫实例失败: {str(e)}")
            raise

    async def _init_browser_environment(self):
        """初始化浏览器环境"""
        try:
            # 导入必要的模块
            from playwright.async_api import async_playwright
            import config.base_config as base_config

            # 启动playwright
            self.playwright = await async_playwright().start()
            chromium = self.playwright.chromium

            # 启动浏览器
            self.browser_context = await self.crawler.launch_browser(
                chromium=chromium,
                playwright_proxy=None,  # 暂时不支持代理
                user_agent=None,
                headless=base_config.HEADLESS
            )

            # 添加stealth脚本
            stealth_js_path = os.path.join(project_root, "libs", "stealth.min.js")
            if os.path.exists(stealth_js_path):
                await self.browser_context.add_init_script(path=stealth_js_path)

            # 创建页面
            self.context_page = await self.browser_context.new_page()

            # 设置爬虫的浏览器环境
            self.crawler.browser_context = self.browser_context
            self.crawler.context_page = self.context_page

            # 导航到目标网站
            if self.platform == "dy":
                await self.context_page.goto("https://www.douyin.com")
            elif self.platform == "xhs":
                # 小红书需要添加特殊cookie
                await self.browser_context.add_cookies([{
                    "name": "webId",
                    "value": "xxx123",
                    "domain": ".xiaohongshu.com",
                    "path": "/",
                }])
                await self.context_page.goto("https://www.xiaohongshu.com")

            self.logger.info("浏览器环境初始化完成")

        except Exception as e:
            self.logger.error(f"初始化浏览器环境失败: {str(e)}")
            raise

    async def _handle_login(self):
        """处理登录"""
        try:
            # 创建客户端
            await self._create_client()

            # 检查是否需要登录
            if hasattr(self.crawler, 'dy_client'):
                client = self.crawler.dy_client
                is_logged_in = await client.pong(browser_context=self.browser_context)
            elif hasattr(self.crawler, 'xhs_client'):
                client = self.crawler.xhs_client
                is_logged_in = await client.pong()
            else:
                raise Exception("无法获取客户端实例")

            if not is_logged_in:
                self._update_progress({
                    "status": "需要登录，正在处理登录...",
                    "percentage": 35,
                    "crawled": 0,
                    "total": 0
                })

                # 执行登录
                await self._perform_login()

                # 更新客户端cookies
                await client.update_cookies(browser_context=self.browser_context)

            self.logger.info("登录状态检查完成")

        except Exception as e:
            self.logger.error(f"处理登录失败: {str(e)}")
            raise

    async def _create_client(self):
        """创建API客户端"""
        try:
            if self.platform == "dy":
                self.crawler.dy_client = await self.crawler.create_douyin_client(None)
            elif self.platform == "xhs":
                self.crawler.xhs_client = await self.crawler.create_xhs_client(None)

            self.logger.info(f"API客户端创建完成: {self.platform}")

        except Exception as e:
            self.logger.error(f"创建API客户端失败: {str(e)}")
            raise

    async def _perform_login(self):
        """执行登录"""
        try:
            import config.base_config as base_config

            if self.platform == "dy":
                from media_platform.douyin.login import DouYinLogin
                login_obj = DouYinLogin(
                    login_type=base_config.LOGIN_TYPE,
                    login_phone="",
                    browser_context=self.browser_context,
                    context_page=self.context_page,
                    cookie_str=base_config.COOKIES
                )
            elif self.platform == "xhs":
                from media_platform.xhs.login import XiaoHongShuLogin
                login_obj = XiaoHongShuLogin(
                    login_type=base_config.LOGIN_TYPE,
                    login_phone="",
                    browser_context=self.browser_context,
                    context_page=self.context_page,
                    cookie_str=base_config.COOKIES
                )
            else:
                raise Exception(f"不支持的平台: {self.platform}")

            await login_obj.begin()
            self.logger.info("登录完成")

        except Exception as e:
            self.logger.error(f"登录失败: {str(e)}")
            raise

    async def _execute_crawling(self, parsed_result: Dict[str, Any]):
        """执行爬取"""
        try:
            if not self.crawler:
                raise Exception("爬虫实例未初始化")

            self.logger.info("开始执行爬取...")

            if self.platform == "dy":
                await self._crawl_douyin(parsed_result)
            elif self.platform == "xhs":
                await self._crawl_xiaohongshu(parsed_result)
            else:
                raise Exception(f"不支持的平台: {self.platform}")

        except Exception as e:
            self.logger.error(f"执行爬取失败: {str(e)}")
            raise
    
    async def _crawl_douyin(self, parsed_result: Dict[str, Any]):
        """爬取抖音数据"""
        try:
            aweme_id = parsed_result.get("id")

            # 处理短链接或无法解析的链接
            if not aweme_id or aweme_id in ["unknown", "short_link"]:
                # 通过访问URL获取真实的视频ID
                aweme_id = await self._resolve_douyin_url()
                if not aweme_id:
                    raise Exception("无法获取有效的视频ID")

            # 获取视频详情
            self._update_progress({
                "status": "获取视频详情...",
                "percentage": 50,
                "crawled": 0,
                "total": 1
            })

            video_detail = await self.crawler.dy_client.get_video_by_id(aweme_id)
            if video_detail:
                # 处理视频信息
                await self._process_douyin_content(video_detail, aweme_id)

            # 获取评论
            if self.config.get("enable_comments", True):
                await self._crawl_douyin_comments(aweme_id)

        except Exception as e:
            self.logger.error(f"爬取抖音数据失败: {str(e)}")
            raise

    async def _resolve_douyin_url(self) -> Optional[str]:
        """解析抖音短链接获取真实视频ID"""
        try:
            if not hasattr(self, 'target_url'):
                return None

            self._update_progress({
                "status": "解析短链接...",
                "percentage": 45,
                "crawled": 0,
                "total": 1
            })

            # 访问URL让浏览器自动重定向
            await self.context_page.goto(self.target_url)

            # 等待页面加载并获取当前URL
            await self.context_page.wait_for_load_state("networkidle", timeout=10000)
            current_url = self.context_page.url

            # 从重定向后的URL中提取视频ID
            match = re.search(r'douyin\.com/video/(\d+)', current_url)
            if match:
                aweme_id = match.group(1)
                self.current_aweme_id = aweme_id
                self.logger.info(f"短链接解析成功: {self.target_url} -> {aweme_id}")
                return aweme_id

            return None

        except Exception as e:
            self.logger.error(f"解析短链接失败: {str(e)}")
            return None

    async def _crawl_xiaohongshu(self, parsed_result: Dict[str, Any]):
        """爬取小红书数据"""
        try:
            note_id = parsed_result.get("id")
            xsec_token = parsed_result.get("xsec_token", "")
            xsec_source = parsed_result.get("xsec_source", "pc_search")

            if not note_id or note_id == "unknown":
                raise Exception("无法获取有效的笔记ID")

            # 获取笔记详情
            self._update_progress({
                "status": "获取笔记详情...",
                "percentage": 50,
                "crawled": 0,
                "total": 1
            })

            note_detail = await self.crawler.xhs_client.get_note_by_id(note_id, xsec_source, xsec_token)
            if note_detail:
                # 处理笔记信息
                await self._process_xiaohongshu_content(note_detail, note_id)

            # 获取评论
            if self.config.get("enable_comments", True):
                await self._crawl_xiaohongshu_comments(note_id, xsec_source, xsec_token)

        except Exception as e:
            self.logger.error(f"爬取小红书数据失败: {str(e)}")
            raise

    async def _process_douyin_content(self, video_detail: Dict[str, Any], aweme_id: str):
        """处理抖音视频内容"""
        try:
            # 提取视频信息
            author_info = video_detail.get("author", {})
            statistics = video_detail.get("statistics", {})

            content_data = {
                "nickname": author_info.get("nickname", ""),
                "user_id": author_info.get("sec_uid", ""),
                "title": video_detail.get("desc", ""),
                "aweme_url": f"https://www.douyin.com/video/{aweme_id}",
                "video_download_url": self._extract_video_download_url(video_detail),
                "like_count": statistics.get("digg_count", 0),
                "comment_count": statistics.get("comment_count", 0),
                "share_count": statistics.get("share_count", 0),
                "create_time": video_detail.get("create_time", ""),
                "processed_time": self._get_current_time()
            }

            self.content_data.append(content_data)
            self._send_data(content_data)

            self.logger.info(f"处理抖音视频内容完成: {content_data.get('title', 'Unknown')}")

        except Exception as e:
            self.logger.error(f"处理抖音视频内容失败: {str(e)}")

    async def _process_xiaohongshu_content(self, note_detail: Dict[str, Any], note_id: str):
        """处理小红书笔记内容"""
        try:
            # 提取笔记信息
            user_info = note_detail.get("user", {})
            interact_info = note_detail.get("interact_info", {})

            content_data = {
                "nickname": user_info.get("nickname", ""),
                "user_id": user_info.get("user_id", ""),
                "title": note_detail.get("title", ""),
                "aweme_url": f"https://www.xiaohongshu.com/explore/{note_id}",
                "video_download_url": "",  # 小红书暂不支持视频下载链接
                "like_count": interact_info.get("liked_count", 0),
                "comment_count": interact_info.get("comment_count", 0),
                "share_count": interact_info.get("share_count", 0),
                "create_time": note_detail.get("time", ""),
                "processed_time": self._get_current_time()
            }

            self.content_data.append(content_data)
            self._send_data(content_data)

            self.logger.info(f"处理小红书笔记内容完成: {content_data.get('title', 'Unknown')}")

        except Exception as e:
            self.logger.error(f"处理小红书笔记内容失败: {str(e)}")
    
    async def _crawl_douyin_comments(self, aweme_id: str):
        """爬取抖音评论"""
        try:
            self._update_progress({
                "status": "开始爬取评论...",
                "percentage": 60,
                "crawled": 0,
                "total": self.config.get("max_comments", 100)
            })

            # 设置评论回调
            async def comment_callback(video_id: str, comments: List[Dict[str, Any]]):
                await self._process_douyin_comments(comments, video_id)

            # 获取所有评论
            await self.crawler.dy_client.get_aweme_all_comments(
                aweme_id=aweme_id,
                crawl_interval=self.config.get("crawl_interval", 2.0),
                is_fetch_sub_comments=self.config.get("enable_sub_comments", False),
                callback=comment_callback,
                max_count=self.config.get("max_comments", 100)
            )

            self.logger.info(f"抖音评论爬取完成: {aweme_id}")

        except Exception as e:
            self.logger.error(f"爬取抖音评论失败: {str(e)}")
            raise

    async def _crawl_xiaohongshu_comments(self, note_id: str, xsec_source: str, xsec_token: str):
        """爬取小红书评论"""
        try:
            self._update_progress({
                "status": "开始爬取评论...",
                "percentage": 60,
                "crawled": 0,
                "total": self.config.get("max_comments", 100)
            })

            # 设置评论回调
            async def comment_callback(note_id: str, comments: List[Dict[str, Any]]):
                await self._process_xiaohongshu_comments(comments, note_id)

            # 获取所有评论 - 小红书需要xsec_token参数
            await self.crawler.xhs_client.get_note_all_comments(
                note_id=note_id,
                xsec_token=xsec_token,
                crawl_interval=self.config.get("crawl_interval", 2.0),
                callback=comment_callback,
                max_count=self.config.get("max_comments", 100)
            )

            self.logger.info(f"小红书评论爬取完成: {note_id}")

        except Exception as e:
            self.logger.error(f"爬取小红书评论失败: {str(e)}")
            raise

    async def _process_douyin_comments(self, comments: List[Dict[str, Any]], aweme_id: str):
        """处理抖音评论数据"""
        try:
            for comment in comments:
                if self.should_stop:
                    break

                # 提取评论信息
                user_info = comment.get("user", {})
                comment_data = {
                    "nickname": user_info.get("nickname", ""),
                    "content": comment.get("text", ""),
                    "aweme_url": f"https://www.douyin.com/video/{aweme_id}",
                    "home_url": f"https://www.douyin.com/user/{user_info.get('sec_uid', '')}",
                    "user_id": user_info.get("sec_uid", ""),
                    "create_time": comment.get("create_time", ""),
                    "like_count": comment.get("digg_count", 0),
                    "reply_count": comment.get("reply_comment_total", 0),
                    "processed_time": self._get_current_time()
                }

                self.comments_data.append(comment_data)
                self.crawled_comments += 1

                # 发送数据
                self._send_data(comment_data)

                # 更新进度
                progress = 60 + (self.crawled_comments / max(self.config.get("max_comments", 100), 1)) * 35
                self._update_progress({
                    "status": f"已爬取 {self.crawled_comments} 条评论",
                    "percentage": min(progress, 95),
                    "crawled": self.crawled_comments,
                    "total": self.config.get("max_comments", 100)
                })

                # 添加延迟
                await asyncio.sleep(random.uniform(0.1, 0.5))

        except Exception as e:
            self.logger.error(f"处理抖音评论失败: {str(e)}")

    async def _process_xiaohongshu_comments(self, comments: List[Dict[str, Any]], note_id: str):
        """处理小红书评论数据"""
        try:
            for comment in comments:
                if self.should_stop:
                    break

                # 提取评论信息
                user_info = comment.get("user_info", {})
                comment_data = {
                    "nickname": user_info.get("nickname", ""),
                    "content": comment.get("content", ""),
                    "aweme_url": f"https://www.xiaohongshu.com/explore/{note_id}",
                    "home_url": f"https://www.xiaohongshu.com/user/profile/{user_info.get('user_id', '')}",
                    "user_id": user_info.get("user_id", ""),
                    "create_time": comment.get("create_time", ""),
                    "like_count": comment.get("like_count", 0),
                    "reply_count": comment.get("sub_comment_count", 0),
                    "processed_time": self._get_current_time()
                }

                self.comments_data.append(comment_data)
                self.crawled_comments += 1

                # 发送数据
                self._send_data(comment_data)

                # 更新进度
                progress = 60 + (self.crawled_comments / max(self.config.get("max_comments", 100), 1)) * 35
                self._update_progress({
                    "status": f"已爬取 {self.crawled_comments} 条评论",
                    "percentage": min(progress, 95),
                    "crawled": self.crawled_comments,
                    "total": self.config.get("max_comments", 100)
                })

                # 添加延迟
                await asyncio.sleep(random.uniform(0.1, 0.5))

        except Exception as e:
            self.logger.error(f"处理小红书评论失败: {str(e)}")

    def _extract_video_download_url(self, video_detail: Dict[str, Any]) -> str:
        """提取视频下载链接"""
        try:
            video_info = video_detail.get("video", {})
            play_addr = video_info.get("play_addr", {})
            url_list = play_addr.get("url_list", [])

            if url_list:
                return url_list[0]
            return ""
        except Exception:
            return ""

    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def _cleanup(self):
        """清理资源"""
        try:
            # 关闭浏览器上下文
            if self.browser_context:
                await self.browser_context.close()
                self.browser_context = None

            # 关闭playwright
            if hasattr(self, 'playwright') and self.playwright:
                await self.playwright.stop()
                self.playwright = None

            self.logger.info("资源清理完成")

        except Exception as e:
            self.logger.error(f"清理资源失败: {str(e)}")

    def _update_progress(self, progress: Dict[str, Any]):
        """更新进度"""
        if self.progress_callback:
            try:
                self.progress_callback(progress)
            except Exception as e:
                self.logger.error(f"进度回调失败: {str(e)}")

    def _send_data(self, data: Dict[str, Any]):
        """发送数据"""
        if self.data_callback:
            try:
                self.data_callback(data)
            except Exception as e:
                self.logger.error(f"数据回调失败: {str(e)}")

    def stop(self):
        """停止爬取"""
        self.should_stop = True
        self.logger.info("收到停止信号")

    def is_crawling(self) -> bool:
        """检查是否正在爬取"""
        return self.is_running

    def get_status(self) -> Dict[str, Any]:
        """获取状态信息"""
        return {
            "is_running": self.is_running,
            "should_stop": self.should_stop,
            "platform": self.platform,
            "config": self.config,
            "total_comments": self.total_comments,
            "crawled_comments": self.crawled_comments
        }

    def get_crawled_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """获取已爬取的数据"""
        return {
            "comments": self.comments_data.copy(),
            "content": self.content_data.copy()
        }
