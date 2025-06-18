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
        required_packages = {
            'pandas': 'pandas',
            'openpyxl': 'openpyxl',
            'PIL': 'Pillow',
            'httpx': 'httpx',
            'playwright': 'playwright',
            'asyncio': None,  # 内置模块
            'tkinter': None,  # 内置模块
            'json': None,     # 内置模块
            'logging': None,  # 内置模块
            'threading': None, # 内置模块
            'datetime': None,  # 内置模块
            'pathlib': None,   # 内置模块
            'typing': None,    # 内置模块
            'urllib': None,    # 内置模块
            're': None,        # 内置模块
            'os': None,        # 内置模块
            'sys': None        # 内置模块
        }

        missing_packages = []

        for module_name, package_name in required_packages.items():
            try:
                __import__(module_name)
                self.logger.debug(f"✓ {module_name} 可用")
            except ImportError:
                if package_name:  # 只有非内置模块才需要安装
                    missing_packages.append(package_name)
                    self.logger.error(f"✗ {module_name} 缺失")

        if missing_packages:
            error_msg = (
                f"缺少必要的依赖包:\n\n"
                f"缺失的包: {', '.join(missing_packages)}\n\n"
                f"请运行以下命令安装:\n"
                f"pip install {' '.join(missing_packages)}\n\n"
                f"或者运行:\n"
                f"pip install -r requirements.txt"
            )
            self.logger.error(error_msg)
            messagebox.showerror("依赖错误", error_msg)
            sys.exit(1)

        self.logger.info("所有依赖检查通过")
    
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
