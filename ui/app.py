#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler UI 应用入口
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import logging

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from ui.main_window import MainWindow


class MediaCrawlerApp:
    """MediaCrawler UI应用类"""
    
    def __init__(self):
        self.main_window = None
        self._setup_logging()
        self._check_dependencies()
    
    def _setup_logging(self):
        """设置日志"""
        log_dir = os.path.join(os.path.dirname(current_dir), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, "ui.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("MediaCrawler UI 应用启动")
    
    def _check_dependencies(self):
        """检查依赖"""
        try:
            import pandas
            import openpyxl
            self.logger.info("依赖检查通过")
        except ImportError as e:
            error_msg = f"缺少必要的依赖包: {str(e)}\n请运行: pip install pandas openpyxl"
            self.logger.error(error_msg)
            messagebox.showerror("依赖错误", error_msg)
            sys.exit(1)
    
    def run(self):
        """运行应用"""
        try:
            self.logger.info("创建主窗口")
            self.main_window = MainWindow()
            
            self.logger.info("启动UI主循环")
            self.main_window.run()
            
        except Exception as e:
            error_msg = f"应用运行时发生错误: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            messagebox.showerror("运行错误", error_msg)
        finally:
            self.logger.info("MediaCrawler UI 应用退出")


def main():
    """主函数"""
    try:
        app = MediaCrawlerApp()
        app.run()
    except KeyboardInterrupt:
        print("\n用户中断程序")
        sys.exit(0)
    except Exception as e:
        print(f"程序启动失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
