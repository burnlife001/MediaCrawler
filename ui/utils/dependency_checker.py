#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖检查器
"""

import sys
import subprocess
from typing import Dict, List, Tuple


class DependencyChecker:
    """依赖检查器类"""
    
    def __init__(self):
        # 定义所有必需的依赖包
        self.required_packages = {
            # UI相关
            'tkinter': {
                'package': None,  # 内置模块
                'description': 'GUI界面库（Python内置）',
                'critical': True
            },
            
            # 数据处理
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
            
            # 图像处理
            'PIL': {
                'package': 'Pillow',
                'description': '图像处理库',
                'critical': True
            },
            
            # 网络请求
            'httpx': {
                'package': 'httpx',
                'description': 'HTTP客户端（短链接解析）',
                'critical': True
            },
            
            # 浏览器自动化
            'playwright': {
                'package': 'playwright',
                'description': '浏览器自动化',
                'critical': True
            },

            # 图像处理（OpenCV）
            'cv2': {
                'package': 'opencv-python',
                'description': '计算机视觉库',
                'critical': True
            },

            # MediaCrawler核心依赖
            'aiofiles': {
                'package': 'aiofiles',
                'description': '异步文件操作',
                'critical': True
            },
            'aiomysql': {
                'package': 'aiomysql',
                'description': 'MySQL异步驱动',
                'critical': False  # UI不直接需要数据库
            },
            'redis': {
                'package': 'redis',
                'description': 'Redis客户端',
                'critical': False  # UI不直接需要Redis
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
            
            # 内置模块
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
        
        print("正在检查依赖包...")
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
            print("所有依赖检查通过！")
            return True, [], []
    
    def check_python_version(self) -> Tuple[bool, str]:
        """检查Python版本"""
        version = sys.version_info
        
        if version.major < 3:
            return False, f"需要Python 3.x，当前版本: {version.major}.{version.minor}.{version.micro}"
        
        if version.minor < 7:
            return False, f"需要Python 3.7+，当前版本: {version.major}.{version.minor}.{version.micro}"
        
        return True, f"Python版本: {version.major}.{version.minor}.{version.micro}"
    
    def generate_install_command(self, missing_packages: List[str]) -> str:
        """生成安装命令"""
        if not missing_packages:
            return ""
        
        return f"pip install {' '.join(missing_packages)}"
    
    def check_pip_available(self) -> bool:
        """检查pip是否可用"""
        try:
            subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def auto_install_packages(self, packages: List[str]) -> Tuple[bool, str]:
        """
        自动安装缺失的包
        
        Args:
            packages: 要安装的包列表
            
        Returns:
            (是否成功, 结果信息)
        """
        if not packages:
            return True, "没有需要安装的包"
        
        if not self.check_pip_available():
            return False, "pip不可用，无法自动安装依赖包"
        
        try:
            print(f"正在安装依赖包: {', '.join(packages)}")
            print("这可能需要几分钟时间...")
            
            cmd = [sys.executable, '-m', 'pip', 'install'] + packages
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            return True, f"成功安装: {', '.join(packages)}"
            
        except subprocess.CalledProcessError as e:
            error_msg = f"安装失败: {e.stderr if e.stderr else str(e)}"
            return False, error_msg
        except Exception as e:
            return False, f"安装过程中发生错误: {str(e)}"
    
    def full_check(self, auto_install: bool = False) -> bool:
        """
        完整的依赖检查
        
        Args:
            auto_install: 是否自动安装缺失的包
            
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
            print("\n✅ 所有依赖检查通过，可以启动MediaCrawler UI")
            return True
        
        print(f"\n❌ 发现 {len(missing_packages)} 个缺失的依赖包")
        
        if auto_install and missing_packages:
            print("\n正在尝试自动安装缺失的依赖包...")
            install_ok, install_msg = self.auto_install_packages(missing_packages)
            print(install_msg)
            
            if install_ok:
                print("\n重新检查依赖...")
                deps_ok, _, _ = self.check_all_dependencies()
                if deps_ok:
                    print("\n✅ 依赖安装成功，可以启动MediaCrawler UI")
                    return True
        
        # 显示手动安装指令
        if missing_packages:
            install_cmd = self.generate_install_command(missing_packages)
            print(f"\n请手动安装缺失的依赖包:")
            print(f"  {install_cmd}")
            print("\n或者运行:")
            print("  pip install -r requirements.txt")
        
        print("\n安装完成后请重新启动程序")
        return False


def main():
    """主函数，用于独立运行依赖检查"""
    checker = DependencyChecker()
    
    # 检查是否传入了自动安装参数
    auto_install = '--auto-install' in sys.argv
    
    success = checker.full_check(auto_install=auto_install)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
