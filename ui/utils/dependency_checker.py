#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI依赖检查器 - 仅检查UI必需的依赖包
"""

import sys
from typing import Dict, List, Tuple


class DependencyChecker:
    """UI依赖检查器类"""

    def __init__(self):
        # 定义UI必需的依赖包（移除了不必要的MediaCrawler核心依赖）
        self.required_packages = {
            # UI界面
            'tkinter': {
                'package': None,  # 内置模块
                'description': 'GUI界面库（Python内置）',
                'critical': True
            },

            # 数据处理和导出
            'pandas': {
                'package': 'pandas',
                'description': '数据处理和Excel导出',
                'critical': True
            },
            'openpyxl': {
                'package': 'openpyxl',
                'description': 'Excel文件读写',
                'critical': True
            },

            # 网络请求（URL解析）
            'httpx': {
                'package': 'httpx',
                'description': 'HTTP客户端（短链接解析）',
                'critical': True
            },

            # MediaCrawler集成必需依赖
            'playwright': {
                'package': 'playwright',
                'description': '浏览器自动化',
                'critical': True
            },
            'pydantic': {
                'package': 'pydantic',
                'description': '数据验证库',
                'critical': True
            },
            'tenacity': {
                'package': 'tenacity',
                'description': '重试机制库',
                'critical': True
            },
            'parsel': {
                'package': 'parsel',
                'description': 'HTML/XML解析器',
                'critical': True
            },
            'execjs': {
                'package': 'pyexecjs',
                'description': 'JavaScript执行引擎',
                'critical': True
            },
            'requests': {
                'package': 'requests',
                'description': 'HTTP请求库',
                'critical': True
            },
            'aiofiles': {
                'package': 'aiofiles',
                'description': '异步文件操作',
                'critical': True
            },

            # 内置模块（仅检查关键的）
            'asyncio': {
                'package': None,
                'description': '异步编程支持',
                'critical': True
            },
            'json': {
                'package': None,
                'description': 'JSON数据处理',
                'critical': True
            },
            'logging': {
                'package': None,
                'description': '日志记录',
                'critical': True
            },
            'threading': {
                'package': None,
                'description': '多线程支持',
                'critical': True
            },
            'datetime': {
                'package': None,
                'description': '日期时间处理',
                'critical': True
            },
            'pathlib': {
                'package': None,
                'description': '路径处理',
                'critical': True
            },
            'typing': {
                'package': None,
                'description': '类型注解',
                'critical': True
            },
            'urllib': {
                'package': None,
                'description': 'URL处理',
                'critical': True
            },
            're': {
                'package': None,
                'description': '正则表达式',
                'critical': True
            },
            'os': {
                'package': None,
                'description': '操作系统接口',
                'critical': True
            },
            'sys': {
                'package': None,
                'description': '系统相关功能',
                'critical': True
            }
        }
    
    def check_all_dependencies(self) -> Tuple[bool, List[str], List[str]]:
        """
        检查所有依赖

        Returns:
            (是否全部通过, 缺失的包列表, 错误信息列表)
        """
        missing_packages = []
        error_messages = []

        print("正在检查UI依赖包...")
        print("=" * 50)

        for module_name, info in self.required_packages.items():
            package_name = info['package']
            description = info['description']
            critical = info['critical']

            try:
                __import__(module_name)
                print(f"✓ {module_name:<12} - {description}")
            except ImportError as e:
                status = "✗ 缺失" if critical else "⚠ 可选"
                print(f"{status} {module_name:<12} - {description}")

                if critical:
                    if package_name:
                        missing_packages.append(package_name)
                    error_messages.append(f"缺失关键模块: {module_name} ({description})")

        print("=" * 50)

        if missing_packages:
            print(f"发现 {len(missing_packages)} 个缺失的依赖包")
            return False, missing_packages, error_messages
        else:
            print("所有UI依赖检查通过！")
            return True, [], []
    
    def check_python_version(self) -> Tuple[bool, str]:
        """检查Python版本"""
        version = sys.version_info

        if version.major < 3:
            return False, f"需要Python 3.x，当前版本: {version.major}.{version.minor}.{version.micro}"

        if version.minor < 7:
            return False, f"需要Python 3.7+，当前版本: {version.major}.{version.minor}.{version.micro}"

        return True, f"Python版本: {version.major}.{version.minor}.{version.micro}"

    def full_check(self, auto_install: bool = False) -> bool:
        """
        完整的UI依赖检查

        Args:
            auto_install: 已废弃，不再支持自动安装

        Returns:
            是否通过检查
        """
        print("MediaCrawler UI 依赖检查")
        print("=" * 60)

        # 检查Python版本
        version_ok, version_msg = self.check_python_version()
        print(f"Python版本检查: {'✓' if version_ok else '✗'} {version_msg}")

        if not version_ok:
            print("\n❌ Python版本不符合要求，请升级到Python 3.7+")
            return False

        print()

        # 检查依赖包
        deps_ok, missing_packages, error_messages = self.check_all_dependencies()

        if deps_ok:
            print("\n✅ 所有UI依赖检查通过，可以启动MediaCrawler UI")
            return True

        print(f"\n❌ 发现 {len(missing_packages)} 个缺失的UI依赖包")

        # 显示安装指令（仅提示使用requirements.txt）
        if missing_packages:
            print(f"\n缺失的依赖包: {', '.join(missing_packages)}")
            print("\n请运行以下命令安装所有依赖:")
            print("  pip install -r requirements.txt")
            print("\n注意：请确保在虚拟环境中运行安装命令")

        print("\n安装完成后请重新启动程序")
        return False


def main():
    """主函数，用于独立运行UI依赖检查"""
    checker = DependencyChecker()

    # 不再支持自动安装参数
    if '--auto-install' in sys.argv or '-a' in sys.argv:
        print("⚠️  注意：不再支持自动安装功能")
        print("请使用: pip install -r requirements.txt")
        print()

    success = checker.full_check(auto_install=False)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
