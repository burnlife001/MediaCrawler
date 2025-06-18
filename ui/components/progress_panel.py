#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进度面板组件
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import time


class ProgressPanel:
    """进度面板类"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # 状态变量
        self.current_status = tk.StringVar(value="空闲状态")
        self.progress_value = tk.DoubleVar(value=0.0)
        self.crawled_count = tk.StringVar(value="0")
        self.total_count = tk.StringVar(value="0")
        self.estimated_time = tk.StringVar(value="--")
        
        # 时间记录
        self.start_time = None
        self.last_update_time = None
        
        # 创建UI
        self._create_widgets()
    
    def _create_widgets(self):
        """创建进度面板UI"""
        # 主框架
        self.frame = ttk.LabelFrame(self.parent, text="进度信息", padding="6")

        # 内容框架
        content_frame = ttk.Frame(self.frame)
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        content_frame.columnconfigure(1, weight=1)

        # 第一行：状态和进度条在同一行
        status_progress_frame = ttk.Frame(content_frame)
        status_progress_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 6))
        status_progress_frame.columnconfigure(1, weight=1)

        # 状态信息
        ttk.Label(status_progress_frame, text="状态:").grid(row=0, column=0, sticky=tk.W, padx=(0, 8))
        self.status_label = ttk.Label(status_progress_frame, textvariable=self.current_status,
                                     foreground="blue", font=("Arial", 9))
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 15))

        # 进度条
        progress_frame = ttk.Frame(status_progress_frame)
        progress_frame.grid(row=0, column=2, sticky=(tk.W, tk.E))
        progress_frame.columnconfigure(0, weight=1)

        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_value,
                                          maximum=100, length=200)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 8))

        self.progress_label = ttk.Label(progress_frame, text="0%", font=("Arial", 9))
        self.progress_label.grid(row=0, column=1)

        # 第二行：统计信息
        stats_frame = ttk.Frame(content_frame)
        stats_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 6))
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(3, weight=1)

        # 已爬取数量
        ttk.Label(stats_frame, text="已爬取:", font=("Arial", 9)).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        count_label = ttk.Label(stats_frame, textvariable=self.crawled_count, foreground="green", font=("Arial", 9))
        count_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))

        # 预计剩余时间
        ttk.Label(stats_frame, text="预计剩余:", font=("Arial", 9)).grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        time_label = ttk.Label(stats_frame, textvariable=self.estimated_time, foreground="orange", font=("Arial", 9))
        time_label.grid(row=0, column=3, sticky=tk.W)

        # 第三行：日志显示区域（紧凑版）
        log_frame = ttk.LabelFrame(content_frame, text="运行日志", padding="4")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S),
                      pady=(0, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        # 创建文本框和滚动条（减小高度）
        self.log_text = tk.Text(log_frame, height=4, width=70, wrap=tk.WORD,
                               font=("Consolas", 8), state="disabled")
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 配置父框架的行权重，让日志区域可以扩展
        content_frame.rowconfigure(2, weight=1)
    
    def update_status(self, status: str, status_type: str = "info"):
        """更新状态信息"""
        self.current_status.set(status)
        
        # 根据状态类型设置颜色
        color_map = {
            "info": "blue",
            "success": "green", 
            "warning": "orange",
            "error": "red"
        }
        color = color_map.get(status_type, "blue")
        self.status_label.config(foreground=color)
        
        # 添加到日志
        self.add_log(f"[{datetime.now().strftime('%H:%M:%S')}] {status}")
    
    def update_progress(self, progress_info: dict):
        """更新进度信息"""
        # 更新进度条
        if "percentage" in progress_info:
            percentage = progress_info["percentage"]
            self.progress_value.set(percentage)
            self.progress_label.config(text=f"{percentage:.1f}%")
        
        # 更新计数
        if "crawled" in progress_info:
            self.crawled_count.set(str(progress_info["crawled"]))
        
        if "total" in progress_info:
            self.total_count.set(str(progress_info["total"]))
        
        # 更新预计时间
        if "estimated_time" in progress_info:
            self.estimated_time.set(progress_info["estimated_time"])
        else:
            self._calculate_estimated_time(progress_info)
        
        # 更新状态
        if "status" in progress_info:
            self.update_status(progress_info["status"])
    
    def _calculate_estimated_time(self, progress_info: dict):
        """计算预计剩余时间"""
        try:
            current_time = time.time()
            
            if self.start_time is None:
                self.start_time = current_time
                return
            
            crawled = progress_info.get("crawled", 0)
            total = progress_info.get("total", 0)
            
            if crawled > 0 and total > 0:
                elapsed_time = current_time - self.start_time
                avg_time_per_item = elapsed_time / crawled
                remaining_items = total - crawled
                estimated_seconds = remaining_items * avg_time_per_item
                
                if estimated_seconds < 60:
                    self.estimated_time.set(f"{int(estimated_seconds)}秒")
                elif estimated_seconds < 3600:
                    minutes = int(estimated_seconds / 60)
                    seconds = int(estimated_seconds % 60)
                    self.estimated_time.set(f"{minutes}分{seconds}秒")
                else:
                    hours = int(estimated_seconds / 3600)
                    minutes = int((estimated_seconds % 3600) / 60)
                    self.estimated_time.set(f"{hours}时{minutes}分")
            else:
                self.estimated_time.set("计算中...")
                
        except Exception:
            self.estimated_time.set("--")
    
    def add_log(self, message: str):
        """添加日志信息"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # 滚动到底部
        self.log_text.config(state="disabled")
        
        # 限制日志行数，避免内存占用过多
        lines = self.log_text.get("1.0", tk.END).split("\n")
        if len(lines) > 1000:  # 保留最近1000行
            self.log_text.config(state="normal")
            self.log_text.delete("1.0", f"{len(lines) - 1000}.0")
            self.log_text.config(state="disabled")
    
    def reset(self):
        """重置进度信息"""
        self.current_status.set("空闲状态")
        self.progress_value.set(0.0)
        self.progress_label.config(text="0%")
        self.crawled_count.set("0")
        self.total_count.set("0")
        self.estimated_time.set("--")

        # 重置时间记录
        self.start_time = None
        self.last_update_time = None

        # 清空日志
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state="disabled")

        # 重置状态标签颜色
        self.status_label.config(foreground="blue")
    
    def set_total_count(self, total: int):
        """设置总数"""
        self.total_count.set(str(total))
    
    def increment_crawled(self, increment: int = 1):
        """增加已爬取数量"""
        current = int(self.crawled_count.get())
        new_count = current + increment
        self.crawled_count.set(str(new_count))
        
        # 更新进度条
        total = int(self.total_count.get())
        if total > 0:
            percentage = (new_count / total) * 100
            self.progress_value.set(percentage)
            self.progress_label.config(text=f"{percentage:.1f}%")
    
    def start_crawling(self):
        """开始爬取时调用"""
        self.start_time = time.time()
        self.update_status("开始爬取", "info")
    
    def finish_crawling(self, success: bool = True):
        """完成爬取时调用"""
        if success:
            self.update_status("爬取完成", "success")
            self.progress_value.set(100.0)
            self.progress_label.config(text="100%")
            self.estimated_time.set("已完成")
        else:
            self.update_status("爬取失败", "error")
    
    def get_log_content(self) -> str:
        """获取日志内容"""
        return self.log_text.get("1.0", tk.END)
