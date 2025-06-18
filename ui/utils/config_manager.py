#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理器
"""

import os
import json
import sys
from typing import Dict, Any
import logging

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)


class ConfigManager:
    """配置管理器类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 配置文件路径
        self.config_dir = os.path.join(project_root, "config")
        self.ui_config_file = os.path.join(self.config_dir, "ui_config.json")
        
        # 默认配置
        self.default_config = {
            "platform": "dy",
            "login_type": "qrcode",
            "enable_comments": True,
            "enable_sub_comments": False,
            "max_comments": 100,
            "crawl_interval": 2.0,
            "proxy_enabled": False,
            "proxy_url": "",
            "auto_export_threshold": 100,
            "export_format": "xlsx",
            "window_geometry": "800x700",
            "last_export_dir": ""
        }
        
        # 当前配置
        self.current_config = self.default_config.copy()
        
        # 加载配置
        self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        try:
            if os.path.exists(self.ui_config_file):
                with open(self.ui_config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                
                # 合并配置（保留默认值，更新已保存的值）
                self.current_config.update(saved_config)
                self.logger.info("配置加载成功")
            else:
                self.logger.info("配置文件不存在，使用默认配置")
                
        except Exception as e:
            self.logger.error(f"加载配置失败: {str(e)}")
            self.current_config = self.default_config.copy()
        
        return self.current_config.copy()
    
    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """保存配置"""
        try:
            # 确保配置目录存在
            os.makedirs(self.config_dir, exist_ok=True)
            
            # 使用传入的配置或当前配置
            config_to_save = config if config is not None else self.current_config
            
            with open(self.ui_config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, ensure_ascii=False, indent=2)
            
            self.logger.info("配置保存成功")
            return True
            
        except Exception as e:
            self.logger.error(f"保存配置失败: {str(e)}")
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return self.current_config.copy()
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """更新配置"""
        try:
            self.current_config.update(updates)
            return self.save_config()
        except Exception as e:
            self.logger.error(f"更新配置失败: {str(e)}")
            return False
    
    def reset_config(self) -> bool:
        """重置为默认配置"""
        try:
            self.current_config = self.default_config.copy()
            return self.save_config()
        except Exception as e:
            self.logger.error(f"重置配置失败: {str(e)}")
            return False
    
    def get_mediacrawler_config(self) -> Dict[str, Any]:
        """获取MediaCrawler原始配置"""
        try:
            # 导入原始配置模块
            import config.base_config as base_config
            
            # 获取当前配置值
            config_dict = {}
            for attr_name in dir(base_config):
                if not attr_name.startswith('_'):
                    config_dict[attr_name] = getattr(base_config, attr_name)
            
            return config_dict
            
        except Exception as e:
            self.logger.error(f"获取MediaCrawler配置失败: {str(e)}")
            return {}
    
    def apply_to_mediacrawler(self, ui_config: Dict[str, Any] = None) -> bool:
        """将UI配置应用到MediaCrawler"""
        try:
            # 使用传入的配置或当前配置
            config = ui_config if ui_config is not None else self.current_config
            
            # 导入配置模块
            import config.base_config as base_config
            
            # 映射UI配置到MediaCrawler配置
            platform_map = {"dy": "dy", "xhs": "xhs"}
            login_type_map = {"qrcode": "qrcode", "cookie": "cookie", "phone": "phone"}
            
            # 设置平台
            if config.get("platform") in platform_map:
                base_config.PLATFORM = platform_map[config["platform"]]
            
            # 设置登录方式
            if config.get("login_type") in login_type_map:
                base_config.LOGIN_TYPE = login_type_map[config["login_type"]]
            
            # 设置评论相关配置
            base_config.ENABLE_GET_COMMENTS = config.get("enable_comments", True)
            base_config.ENABLE_GET_SUB_COMMENTS = config.get("enable_sub_comments", False)
            base_config.CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = config.get("max_comments", 100)
            
            # 设置爬取间隔
            base_config.CRAWLER_MAX_SLEEP_SEC = config.get("crawl_interval", 2.0)
            
            # 设置代理
            base_config.ENABLE_IP_PROXY = config.get("proxy_enabled", False)
            
            # 设置数据保存格式
            base_config.SAVE_DATA_OPTION = "json"  # UI版本固定使用JSON格式
            
            # 设置爬取类型为详情模式
            base_config.CRAWLER_TYPE = "detail"
            
            self.logger.info("UI配置已应用到MediaCrawler")
            return True
            
        except Exception as e:
            self.logger.error(f"应用配置到MediaCrawler失败: {str(e)}")
            return False
    
    def create_temp_config(self, url: str, platform: str, ui_config: Dict[str, Any]) -> bool:
        """创建临时配置用于单次爬取"""
        try:
            # 应用基础配置
            self.apply_to_mediacrawler(ui_config)
            
            # 导入配置模块
            import config.base_config as base_config
            
            # 根据平台和URL设置特定配置
            if platform == "dy":
                # 从URL解析出aweme_id
                from ui.controllers.url_parser import URLParser
                parser = URLParser()
                parsed = parser.parse_url(url, platform)
                
                if parsed and parsed.get("id") != "unknown":
                    base_config.DY_SPECIFIED_ID_LIST = [parsed["id"]]
                else:
                    # 如果是短链接，需要特殊处理
                    base_config.DY_SPECIFIED_ID_LIST = []
                    
            elif platform == "xhs":
                # 小红书需要完整URL
                base_config.XHS_SPECIFIED_NOTE_URL_LIST = [url]
            
            self.logger.info(f"临时配置创建成功: {platform}, {url}")
            return True
            
        except Exception as e:
            self.logger.error(f"创建临时配置失败: {str(e)}")
            return False
    
    def get_export_settings(self) -> Dict[str, Any]:
        """获取导出设置"""
        return {
            "auto_export_threshold": self.current_config.get("auto_export_threshold", 100),
            "export_format": self.current_config.get("export_format", "xlsx"),
            "last_export_dir": self.current_config.get("last_export_dir", "")
        }
    
    def update_export_settings(self, settings: Dict[str, Any]) -> bool:
        """更新导出设置"""
        export_keys = ["auto_export_threshold", "export_format", "last_export_dir"]
        updates = {k: v for k, v in settings.items() if k in export_keys}
        return self.update_config(updates)
    
    def get_window_settings(self) -> Dict[str, Any]:
        """获取窗口设置"""
        return {
            "geometry": self.current_config.get("window_geometry", "800x700")
        }
    
    def update_window_settings(self, settings: Dict[str, Any]) -> bool:
        """更新窗口设置"""
        window_keys = ["window_geometry"]
        updates = {k: v for k, v in settings.items() if k in window_keys}
        return self.update_config(updates)
    
    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, str]:
        """验证配置的有效性"""
        try:
            # 验证平台
            if config.get("platform") not in ["dy", "xhs"]:
                return False, "无效的平台设置"
            
            # 验证登录类型
            if config.get("login_type") not in ["qrcode", "cookie", "phone"]:
                return False, "无效的登录类型"
            
            # 验证数值范围
            max_comments = config.get("max_comments", 100)
            if not isinstance(max_comments, int) or max_comments <= 0 or max_comments > 10000:
                return False, "最大评论数必须在1-10000之间"
            
            crawl_interval = config.get("crawl_interval", 2.0)
            if not isinstance(crawl_interval, (int, float)) or crawl_interval < 0.1 or crawl_interval > 60:
                return False, "爬取间隔必须在0.1-60秒之间"
            
            return True, "配置验证通过"
            
        except Exception as e:
            return False, f"配置验证失败: {str(e)}"
