#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI功能测试脚本
"""

import asyncio
import sys
import os

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from ui.controllers.url_parser import URLParser
from ui.controllers.data_processor import DataProcessor
from ui.utils.config_manager import ConfigManager


async def test_url_parser():
    """测试URL解析器"""
    print("=" * 50)
    print("测试URL解析器")
    print("=" * 50)
    
    parser = URLParser()
    
    # 测试抖音URL
    dy_urls = [
        "https://www.douyin.com/video/7234567890123456789",
        "https://v.douyin.com/AbCdEfG/",
    ]
    
    for url in dy_urls:
        print(f"\n测试抖音URL: {url}")
        is_valid, message = parser.validate_url(url, "dy")
        print(f"验证结果: {is_valid}, 消息: {message}")
        
        if is_valid:
            result = parser.parse_url(url, "dy")
            print(f"解析结果: {result}")
    
    # 测试小红书URL
    xhs_urls = [
        "https://www.xiaohongshu.com/explore/64a1b2c3d4e5f6789012345a",
        "https://www.xiaohongshu.com/explore/64a1b2c3d4e5f6789012345a?xsec_token=xxx&xsec_source=pc_search"
    ]
    
    for url in xhs_urls:
        print(f"\n测试小红书URL: {url}")
        is_valid, message = parser.validate_url(url, "xhs")
        print(f"验证结果: {is_valid}, 消息: {message}")
        
        if is_valid:
            result = parser.parse_url(url, "xhs")
            print(f"解析结果: {result}")


def test_data_processor():
    """测试数据处理器"""
    print("\n" + "=" * 50)
    print("测试数据处理器")
    print("=" * 50)
    
    processor = DataProcessor()
    
    # 测试数据
    test_data = [
        {
            "nickname": "测试用户1",
            "content": "这是一条测试评论",
            "aweme_url": "https://www.douyin.com/video/123456789",
            "home_url": "https://www.douyin.com/user/test1",
            "like_count": 10,
            "reply_count": 2
        },
        {
            "nickname": "测试用户2", 
            "content": "这是另一条测试评论",
            "aweme_url": "https://www.douyin.com/video/123456789",
            "home_url": "https://www.douyin.com/user/test2",
            "like_count": 5,
            "reply_count": 1
        }
    ]
    
    # 添加测试数据
    for data in test_data:
        processor.add_data(data)
    
    print(f"数据数量: {processor.get_data_count()}")
    print(f"统计信息: {processor.get_statistics()}")
    
    # 测试导出
    try:
        file_path = processor.export_to_excel("test_export.xlsx")
        print(f"导出成功: {file_path}")
    except Exception as e:
        print(f"导出失败: {str(e)}")


def test_config_manager():
    """测试配置管理器"""
    print("\n" + "=" * 50)
    print("测试配置管理器")
    print("=" * 50)
    
    config_manager = ConfigManager()
    
    # 获取当前配置
    config = config_manager.get_config()
    print(f"当前配置: {config}")
    
    # 测试配置验证
    is_valid, message = config_manager.validate_config(config)
    print(f"配置验证: {is_valid}, 消息: {message}")
    
    # 测试更新配置
    updates = {
        "platform": "xhs",
        "max_comments": 50
    }
    success = config_manager.update_config(updates)
    print(f"更新配置: {success}")
    
    # 获取更新后的配置
    new_config = config_manager.get_config()
    print(f"更新后配置: {new_config}")


async def main():
    """主函数"""
    print("MediaCrawler UI 功能测试")
    print("=" * 60)
    
    try:
        # 测试URL解析器
        await test_url_parser()
        
        # 测试数据处理器
        test_data_processor()
        
        # 测试配置管理器
        test_config_manager()
        
        print("\n" + "=" * 60)
        print("所有测试完成！")
        
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
