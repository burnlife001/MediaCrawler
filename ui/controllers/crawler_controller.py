#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫控制器
"""

import asyncio
import sys
import os
from typing import Dict, Any, Callable, Optional
import logging

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)


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
    
    async def crawl_by_url(self, url: str):
        """根据URL爬取数据"""
        try:
            self.is_running = True
            self.should_stop = False
            
            # 更新进度
            self._update_progress({
                "status": "初始化爬虫...",
                "percentage": 0,
                "crawled": 0,
                "total": 0
            })
            
            # 应用配置到MediaCrawler
            from ui.utils.config_manager import ConfigManager
            config_manager = ConfigManager()
            config_manager.create_temp_config(url, self.platform, self.config)
            
            # 更新进度
            self._update_progress({
                "status": "启动爬虫引擎...",
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
                "status": "开始爬取数据...",
                "percentage": 20,
                "crawled": 0,
                "total": 1
            })
            
            # 执行爬取
            await self._execute_crawling()
            
            # 完成
            if not self.should_stop:
                self._update_progress({
                    "status": "爬取完成",
                    "percentage": 100,
                    "crawled": 1,
                    "total": 1
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
            self.is_running = False
    
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
    
    async def _execute_crawling(self):
        """执行爬取"""
        try:
            if not self.crawler:
                raise Exception("爬虫实例未初始化")
            
            # 这里是一个简化的实现
            # 实际应该调用爬虫的具体方法
            self.logger.info("开始执行爬取...")
            
            # 模拟爬取过程
            await self._simulate_crawling()
            
        except Exception as e:
            self.logger.error(f"执行爬取失败: {str(e)}")
            raise
    
    async def _simulate_crawling(self):
        """模拟爬取过程（临时实现）"""
        # 这是一个临时的模拟实现
        # 在阶段2中会替换为真实的爬虫集成
        
        total_steps = 10
        for i in range(total_steps):
            if self.should_stop:
                break
            
            # 模拟处理时间
            await asyncio.sleep(1)
            
            # 更新进度
            progress = 20 + (i + 1) * 8  # 从20%到100%
            self._update_progress({
                "status": f"正在爬取第 {i + 1} 条数据...",
                "percentage": progress,
                "crawled": i + 1,
                "total": total_steps
            })
            
            # 模拟数据回调
            if i < 5:  # 只模拟前5条数据
                mock_data = {
                    "nickname": f"用户{i + 1}",
                    "content": f"这是第{i + 1}条模拟评论内容，用于测试UI界面的数据显示功能。",
                    "aweme_url": f"https://www.douyin.com/video/123456789{i}",
                    "home_url": f"https://www.douyin.com/user/user{i + 1}",
                    "create_time": "2024-01-01 12:00:00",
                    "like_count": (i + 1) * 10,
                    "reply_count": i + 1
                }
                self._send_data(mock_data)
    
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
            "config": self.config
        }
