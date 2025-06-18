#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler UI 启动脚本
"""

import sys
import os

# 确保当前目录在Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 导入并运行UI应用
from ui.app import main

if __name__ == "__main__":
    print("=" * 60)
    print("MediaCrawler - 评论提取工具 UI版本")
    print("=" * 60)
    print("正在启动图形界面...")
    print()
    
    main()
