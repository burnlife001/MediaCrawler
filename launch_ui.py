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

# 导入并运行UI启动脚本
if __name__ == "__main__":
    try:
        from ui.scripts.launch_ui import main
        main()
    except ImportError:
        print("❌ 无法导入UI模块，请检查项目结构")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        sys.exit(1)
