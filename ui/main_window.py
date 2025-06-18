#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler UI 主窗口
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import asyncio
from typing import Optional, Callable

from .components.config_panel import ConfigPanel
from .components.progress_panel import ProgressPanel
from .components.result_panel import ResultPanel
from .controllers.url_parser import URLParser
from .controllers.crawler_controller import CrawlerController
from .controllers.data_processor import DataProcessor
from .utils.config_manager import ConfigManager


class MainWindow:
    """MediaCrawler 主窗口类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MediaCrawler - 评论提取工具")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # 初始化组件
        self.url_parser = URLParser()
        self.config_manager = ConfigManager()
        self.data_processor = DataProcessor()
        self.crawler_controller = None  # 延迟初始化
        
        # 状态变量
        self.is_crawling = False
        self.current_platform = tk.StringVar(value="dy")  # dy=抖音, xhs=小红书
        self.video_url = tk.StringVar()
        
        # 创建UI组件
        self._create_widgets()
        self._setup_layout()
        self._bind_events()
        
        # 初始化配置
        self._load_config()
    
    def _create_widgets(self):
        """创建UI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置根窗口的网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # 1. 平台选择区域
        platform_frame = ttk.LabelFrame(main_frame, text="平台选择", padding="5")
        platform_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        platform_frame.columnconfigure(1, weight=1)
        
        ttk.Radiobutton(platform_frame, text="抖音", variable=self.current_platform, 
                       value="dy").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(platform_frame, text="小红书", variable=self.current_platform, 
                       value="xhs").grid(row=0, column=1, sticky=tk.W)
        
        # 2. 链接输入区域
        url_frame = ttk.LabelFrame(main_frame, text="视频链接", padding="5")
        url_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(0, weight=1)
        
        self.url_entry = ttk.Entry(url_frame, textvariable=self.video_url, 
                                  font=("Arial", 10))
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.parse_btn = ttk.Button(url_frame, text="解析", command=self._parse_url)
        self.parse_btn.grid(row=0, column=1)
        
        # URL状态标签
        self.url_status_label = ttk.Label(url_frame, text="", foreground="gray")
        self.url_status_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # 3. 配置面板
        self.config_panel = ConfigPanel(main_frame)
        self.config_panel.frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 4. 操作按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.start_btn = ttk.Button(button_frame, text="开始爬取", 
                                   command=self._start_crawling)
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="停止", 
                                  command=self._stop_crawling, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.export_btn = ttk.Button(button_frame, text="导出数据", 
                                    command=self._export_data)
        self.export_btn.grid(row=0, column=2, padx=(0, 10))
        
        self.clear_btn = ttk.Button(button_frame, text="清空结果", 
                                   command=self._clear_results)
        self.clear_btn.grid(row=0, column=3)
        
        # 5. 进度面板
        self.progress_panel = ProgressPanel(main_frame)
        self.progress_panel.frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 6. 结果面板
        self.result_panel = ResultPanel(main_frame)
        self.result_panel.frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0))
        
        # 配置行权重，让结果面板可以扩展
        main_frame.rowconfigure(5, weight=1)
    
    def _setup_layout(self):
        """设置布局"""
        pass  # 布局已在_create_widgets中设置
    
    def _bind_events(self):
        """绑定事件"""
        # 绑定URL输入框的实时验证
        self.video_url.trace('w', self._on_url_change)
        
        # 绑定平台切换事件
        self.current_platform.trace('w', self._on_platform_change)
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _load_config(self):
        """加载配置"""
        # 从配置管理器加载用户设置
        config = self.config_manager.get_config()
        self.current_platform.set(config.get('platform', 'dy'))
        self.config_panel.load_config(config)
    
    def _on_url_change(self, *args):
        """URL输入变化时的回调"""
        text = self.video_url.get().strip()
        if not text:
            self.url_status_label.config(text="", foreground="gray")
            return

        # 实时验证URL格式
        platform = self.current_platform.get()
        is_valid, message = self.url_parser.validate_url(text, platform)

        if is_valid:
            # 尝试提取URL显示更详细的信息
            extracted_url = self.url_parser.extract_url_from_text(text, platform)
            if extracted_url and len(text) > len(extracted_url) + 10:
                self.url_status_label.config(text=f"✓ 已识别分享链接: {extracted_url[:50]}...", foreground="green")
            else:
                self.url_status_label.config(text="✓ 链接格式正确", foreground="green")
        else:
            self.url_status_label.config(text=f"✗ {message}", foreground="red")
    
    def _on_platform_change(self, *args):
        """平台切换时的回调"""
        # 重新验证当前URL
        self._on_url_change()
        
        # 更新配置面板的平台相关设置
        platform = self.current_platform.get()
        self.config_panel.on_platform_change(platform)
    
    def _parse_url(self):
        """解析URL"""
        text = self.video_url.get().strip()
        platform = self.current_platform.get()

        if not text:
            messagebox.showwarning("警告", "请输入视频链接或分享文本")
            return

        try:
            result = self.url_parser.parse_url(text, platform)
            if result:
                # 构建解析结果信息
                info_parts = []
                if result.get('id', 'Unknown') != 'unknown':
                    info_parts.append(f"视频ID: {result.get('id', 'Unknown')}")

                if result.get('extracted_url'):
                    info_parts.append(f"提取的链接: {result.get('extracted_url')}")

                if result.get('needs_redirect'):
                    info_parts.append("注意: 这是短链接，爬取时会自动解析")

                info_text = "\n".join(info_parts) if info_parts else f"视频ID: {result.get('id', 'Unknown')}"

                self.url_status_label.config(
                    text=f"✓ 解析成功: {result.get('id', 'Unknown')}",
                    foreground="green"
                )
                messagebox.showinfo("解析成功", info_text)
            else:
                self.url_status_label.config(text="✗ 解析失败", foreground="red")
                messagebox.showerror("解析失败", "无法解析该链接或文本")
        except Exception as e:
            self.url_status_label.config(text="✗ 解析错误", foreground="red")
            messagebox.showerror("错误", f"解析过程中发生错误: {str(e)}")
    
    def _start_crawling(self):
        """开始爬取"""
        # 验证输入
        text = self.video_url.get().strip()
        platform = self.current_platform.get()

        if not text:
            messagebox.showwarning("警告", "请输入视频链接或分享文本")
            return

        # 验证URL
        is_valid, message = self.url_parser.validate_url(text, platform)
        if not is_valid:
            messagebox.showerror("错误", f"链接格式错误: {message}")
            return

        # 提取实际的URL用于爬取
        extracted_url = self.url_parser.extract_url_from_text(text, platform)
        actual_url = extracted_url if extracted_url else text
        
        # 获取配置
        config = self.config_panel.get_config()
        
        # 更新UI状态
        self.is_crawling = True
        self._update_button_states()
        
        # 重置进度和结果
        self.progress_panel.reset()
        self.data_processor.reset()
        
        # 在新线程中启动爬取
        threading.Thread(target=self._run_crawler, args=(actual_url, platform, config),
                        daemon=True).start()
    
    def _stop_crawling(self):
        """停止爬取"""
        if self.crawler_controller:
            self.crawler_controller.stop()
        
        self.is_crawling = False
        self._update_button_states()
        self.progress_panel.update_status("已停止")
    
    def _export_data(self):
        """导出数据"""
        try:
            file_path = self.data_processor.export_to_excel()
            if file_path:
                messagebox.showinfo("导出成功", f"数据已导出到: {file_path}")
            else:
                messagebox.showwarning("警告", "没有数据可导出")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def _clear_results(self):
        """清空结果"""
        if messagebox.askyesno("确认", "确定要清空所有结果吗？"):
            self.data_processor.clear()
            self.result_panel.clear()
            self.progress_panel.reset()
    
    def _update_button_states(self):
        """更新按钮状态"""
        if self.is_crawling:
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
        else:
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
    
    def _run_crawler(self, url: str, platform: str, config: dict):
        """在新线程中运行爬虫"""
        try:
            # 创建新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # 初始化爬虫控制器
            self.crawler_controller = CrawlerController(
                platform=platform,
                config=config,
                progress_callback=self._on_progress_update,
                data_callback=self._on_data_received
            )
            
            # 运行爬虫
            loop.run_until_complete(self.crawler_controller.crawl_by_url(url))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"爬取失败: {str(e)}"))
        finally:
            # 更新UI状态
            self.is_crawling = False
            self.root.after(0, self._update_button_states)
            self.root.after(0, lambda: self.progress_panel.update_status("完成"))
    
    def _on_progress_update(self, progress: dict):
        """进度更新回调"""
        self.root.after(0, lambda: self.progress_panel.update_progress(progress))
    
    def _on_data_received(self, data: dict):
        """数据接收回调"""
        self.root.after(0, lambda: self._process_new_data(data))
    
    def _process_new_data(self, data: dict):
        """处理新接收的数据"""
        # 添加到数据处理器
        self.data_processor.add_data(data)
        
        # 更新结果面板
        self.result_panel.add_data(data)
        
        # 检查是否需要自动导出
        if self.data_processor.should_auto_export():
            try:
                file_path = self.data_processor.auto_export()
                self.progress_panel.update_status(f"已自动导出到: {file_path}")
            except Exception as e:
                self.progress_panel.update_status(f"自动导出失败: {str(e)}")
    
    def _on_closing(self):
        """窗口关闭时的处理"""
        if self.is_crawling:
            if messagebox.askyesno("确认", "正在爬取中，确定要退出吗？"):
                self._stop_crawling()
                self.root.after(1000, self.root.destroy)  # 延迟销毁窗口
        else:
            self.root.destroy()
    
    def run(self):
        """运行主窗口"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
