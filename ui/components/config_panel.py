#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置面板组件
"""

import tkinter as tk
from tkinter import ttk


class ConfigPanel:
    """配置面板类"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # 配置变量
        self.login_type = tk.StringVar(value="qrcode")
        self.enable_comments = tk.BooleanVar(value=True)
        self.enable_sub_comments = tk.BooleanVar(value=False)
        self.max_comments = tk.StringVar(value="100")
        self.crawl_interval = tk.StringVar(value="2")
        self.proxy_enabled = tk.BooleanVar(value=False)
        self.proxy_url = tk.StringVar()
        
        # 创建UI
        self._create_widgets()
    
    def _create_widgets(self):
        """创建配置面板UI"""
        # 主框架 - 可折叠的配置设置
        self.frame = ttk.LabelFrame(self.parent, text="配置设置", padding="5")
        
        # 创建内容框架
        content_frame = ttk.Frame(self.frame)
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        content_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # 登录方式设置
        login_frame = ttk.LabelFrame(content_frame, text="登录方式", padding="5")
        login_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(login_frame, text="二维码登录", variable=self.login_type, 
                       value="qrcode").grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Radiobutton(login_frame, text="Cookie登录", variable=self.login_type, 
                       value="cookie").grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        ttk.Radiobutton(login_frame, text="手机号登录", variable=self.login_type, 
                       value="phone").grid(row=0, column=2, sticky=tk.W)
        
        row += 1
        
        # 评论设置
        comment_frame = ttk.LabelFrame(content_frame, text="评论设置", padding="5")
        comment_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        comment_frame.columnconfigure(1, weight=1)
        
        # 第一行：获取评论和二级评论
        ttk.Checkbutton(comment_frame, text="获取评论", 
                       variable=self.enable_comments).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Checkbutton(comment_frame, text="获取二级评论", 
                       variable=self.enable_sub_comments).grid(row=0, column=1, sticky=tk.W)
        
        # 第二行：最大评论数
        ttk.Label(comment_frame, text="最大评论数:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        comments_frame = ttk.Frame(comment_frame)
        comments_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 0), padx=(10, 0))
        
        self.max_comments_entry = ttk.Entry(comments_frame, textvariable=self.max_comments, width=10)
        self.max_comments_entry.grid(row=0, column=0, sticky=tk.W)
        ttk.Label(comments_frame, text="条").grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        row += 1
        
        # 爬取设置
        crawl_frame = ttk.LabelFrame(content_frame, text="爬取设置", padding="5")
        crawl_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        crawl_frame.columnconfigure(1, weight=1)
        
        # 爬取间隔
        ttk.Label(crawl_frame, text="爬取间隔:").grid(row=0, column=0, sticky=tk.W)
        interval_frame = ttk.Frame(crawl_frame)
        interval_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        self.crawl_interval_entry = ttk.Entry(interval_frame, textvariable=self.crawl_interval, width=10)
        self.crawl_interval_entry.grid(row=0, column=0, sticky=tk.W)
        ttk.Label(interval_frame, text="秒").grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        row += 1
        
        # 代理设置
        proxy_frame = ttk.LabelFrame(content_frame, text="代理设置", padding="5")
        proxy_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        proxy_frame.columnconfigure(1, weight=1)
        
        ttk.Checkbutton(proxy_frame, text="启用代理", 
                       variable=self.proxy_enabled, 
                       command=self._on_proxy_toggle).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(proxy_frame, text="代理地址:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.proxy_entry = ttk.Entry(proxy_frame, textvariable=self.proxy_url, state="disabled")
        self.proxy_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(5, 0))
        
        # 绑定事件
        self._bind_events()
    
    def _bind_events(self):
        """绑定事件"""
        # 绑定评论开关，控制相关选项的可用性
        self.enable_comments.trace('w', self._on_comments_toggle)
        
        # 绑定数值输入验证
        self.max_comments.trace('w', self._validate_max_comments)
        self.crawl_interval.trace('w', self._validate_crawl_interval)
    
    def _on_comments_toggle(self, *args):
        """评论开关切换时的处理"""
        enabled = self.enable_comments.get()
        
        # 控制二级评论选项的可用性
        if not enabled:
            self.enable_sub_comments.set(False)
        
        # 这里可以添加更多的联动逻辑
    
    def _on_proxy_toggle(self):
        """代理开关切换时的处理"""
        enabled = self.proxy_enabled.get()
        state = "normal" if enabled else "disabled"
        self.proxy_entry.config(state=state)
        
        if not enabled:
            self.proxy_url.set("")
    
    def _validate_max_comments(self, *args):
        """验证最大评论数输入"""
        value = self.max_comments.get()
        if value and not value.isdigit():
            # 移除非数字字符
            cleaned = ''.join(c for c in value if c.isdigit())
            self.max_comments.set(cleaned)
    
    def _validate_crawl_interval(self, *args):
        """验证爬取间隔输入"""
        value = self.crawl_interval.get()
        if value:
            try:
                float(value)
            except ValueError:
                # 移除无效字符，保留数字和小数点
                cleaned = ''.join(c for c in value if c.isdigit() or c == '.')
                # 确保只有一个小数点
                if cleaned.count('.') > 1:
                    parts = cleaned.split('.')
                    cleaned = parts[0] + '.' + ''.join(parts[1:])
                self.crawl_interval.set(cleaned)
    
    def get_config(self) -> dict:
        """获取当前配置"""
        return {
            'login_type': self.login_type.get(),
            'enable_comments': self.enable_comments.get(),
            'enable_sub_comments': self.enable_sub_comments.get(),
            'max_comments': int(self.max_comments.get()) if self.max_comments.get().isdigit() else 100,
            'crawl_interval': float(self.crawl_interval.get()) if self.crawl_interval.get() else 2.0,
            'proxy_enabled': self.proxy_enabled.get(),
            'proxy_url': self.proxy_url.get() if self.proxy_enabled.get() else None
        }
    
    def load_config(self, config: dict):
        """加载配置"""
        self.login_type.set(config.get('login_type', 'qrcode'))
        self.enable_comments.set(config.get('enable_comments', True))
        self.enable_sub_comments.set(config.get('enable_sub_comments', False))
        self.max_comments.set(str(config.get('max_comments', 100)))
        self.crawl_interval.set(str(config.get('crawl_interval', 2.0)))
        self.proxy_enabled.set(config.get('proxy_enabled', False))
        self.proxy_url.set(config.get('proxy_url', ''))
        
        # 更新代理输入框状态
        self._on_proxy_toggle()
    
    def on_platform_change(self, platform: str):
        """平台切换时的处理"""
        # 根据不同平台调整默认设置
        if platform == "dy":  # 抖音
            # 抖音的默认设置
            pass
        elif platform == "xhs":  # 小红书
            # 小红书的默认设置
            pass
    
    def validate(self) -> tuple[bool, str]:
        """验证配置的有效性"""
        # 验证最大评论数
        try:
            max_comments = int(self.max_comments.get())
            if max_comments <= 0:
                return False, "最大评论数必须大于0"
            if max_comments > 10000:
                return False, "最大评论数不能超过10000"
        except ValueError:
            return False, "最大评论数必须是有效数字"
        
        # 验证爬取间隔
        try:
            interval = float(self.crawl_interval.get())
            if interval < 0.1:
                return False, "爬取间隔不能小于0.1秒"
            if interval > 60:
                return False, "爬取间隔不能超过60秒"
        except ValueError:
            return False, "爬取间隔必须是有效数字"
        
        # 验证代理设置
        if self.proxy_enabled.get():
            proxy_url = self.proxy_url.get().strip()
            if not proxy_url:
                return False, "启用代理时必须填写代理地址"
            # 这里可以添加更详细的代理URL格式验证
        
        return True, "配置验证通过"
