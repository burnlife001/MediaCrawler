#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler UI 启动脚本
"""

import sys
import os

# 确保项目根目录在Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def check_dependencies():
    """检查依赖"""
    try:
        from ui.utils.dependency_checker import DependencyChecker

        checker = DependencyChecker()

        # 不再支持自动安装参数
        auto_install = '--auto-install' in sys.argv or '-a' in sys.argv
        if auto_install:
            print("⚠️  注意：不再支持自动安装功能")
            print("请使用: pip install -r requirements.txt")
            print()

        return checker.full_check(auto_install=False)

    except ImportError:
        # 如果连依赖检查器都无法导入，说明基础模块有问题
        print("❌ 无法导入依赖检查器，请检查Python环境")
        return False
    except Exception as e:
        print(f"❌ 依赖检查过程中发生错误: {str(e)}")
        return False

def main():
    """主函数"""
    try:
        print("=" * 60)
        print("MediaCrawler - 评论提取工具 UI版本")
        print("=" * 60)

        # 首先进行依赖检查
        if not check_dependencies():
            print("\n❌ UI依赖检查失败，无法启动程序")
            print("\n请运行以下命令安装依赖:")
            print("  pip install -r requirements.txt")
            print("\n注意：请确保在虚拟环境中运行安装命令")
            input("\n按回车键退出...")
            sys.exit(1)

        print("\n正在启动图形界面...")
        print()

        # 导入并启动UI应用
        from ui.app import MediaCrawlerApp

        app = MediaCrawlerApp()
        app.run()

    except KeyboardInterrupt:
        print("\n用户中断，程序退出")
    except Exception as e:
        print(f"启动失败: {str(e)}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")

if __name__ == "__main__":
    main()
