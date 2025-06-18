#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音数据提取脚本
支持4种类型的JSON文件数据提取：
1. detail_comments - 详情页评论数据
2. search_comments - 搜索页评论数据
3. detail_contents - 详情页内容数据
4. search_contents - 搜索页内容数据
"""

import json
import pandas as pd
import os
from pathlib import Path

def get_file_type(filename):
    """
    根据文件名判断文件类型
    """
    filename = filename.lower()
    if filename.startswith('detail_comments'):
        return 'detail_comments'
    elif filename.startswith('search_comments'):
        return 'search_comments'
    elif filename.startswith('detail_contents'):
        return 'detail_contents'
    elif filename.startswith('search_contents'):
        return 'search_contents'
    else:
        return 'unknown'

def extract_comments_data(item):
    """
    提取评论类型数据的字段
    """
    # 构建home_url和aweme_url
    sec_uid = item.get('sec_uid', '')
    aweme_id = item.get('aweme_id', '')

    home_url = f"https://www.douyin.com/user/{sec_uid}" if sec_uid else ''
    aweme_url = f"https://www.douyin.com/video/{aweme_id}" if aweme_id else ''

    return {
        'nickname': item.get('nickname', ''),
        'content': item.get('content', ''),
        'aweme_url': aweme_url,
        'home_url': home_url
    }

def extract_contents_data(item):
    """
    提取内容类型数据的字段
    """
    return {
        'nickname': item.get('nickname', ''),
        'user_id': item.get('user_id', ''),
        'title': item.get('title', ''),
        'aweme_url': item.get('aweme_url', ''),
        'video_download_url': item.get('video_download_url', '')
    }

def extract_douyin_data(json_file):
    """
    从JSON文件中提取抖音数据并保存到Excel文件
    """
    # 检查文件是否存在
    if not json_file.exists():
        print(f"错误：找不到文件 {json_file}")
        return

    # 判断文件类型
    file_type = get_file_type(json_file.name)
    if file_type == 'unknown':
        print(f"警告：未识别的文件类型 {json_file.name}，跳过处理")
        return

    print(f"\n处理文件：{json_file.name}")
    print(f"文件类型：{file_type}")

    try:
        # 读取JSON文件
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"成功读取JSON文件，共有 {len(data)} 条记录")

        # 根据文件类型提取不同的字段
        extracted_data = []
        for item in data:
            if file_type in ['detail_comments', 'search_comments']:
                extracted_item = extract_comments_data(item)
            elif file_type in ['detail_contents', 'search_contents']:
                extracted_item = extract_contents_data(item)

            extracted_data.append(extracted_item)

        # 创建DataFrame
        df = pd.DataFrame(extracted_data)
        # 输出Excel文件路径
        excel_file = json_file.parent / f"{json_file.stem}.xlsx"
        # 保存到Excel文件
        df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"数据提取完成！")
        print(f"Excel文件已保存到：{excel_file}")
        print(f"共提取 {len(extracted_data)} 条记录")
        # 显示前几行数据预览
        print("\n数据预览：")
        print(df.head())
        # 显示各字段的统计信息
        print("\n字段统计：")
        for column in df.columns:
            non_empty_count = df[column].astype(str).str.strip().ne('').sum()
            print(f"{column}: {non_empty_count}/{len(df)} 条记录有值")

    except json.JSONDecodeError as e:
        print(f"JSON文件解析错误：{e}")
    except Exception as e:
        print(f"处理过程中发生错误：{e}")


def main(json_dir_path):
    """主函数"""
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    # JSON文件目录
    if isinstance(json_dir_path, str):
        json_dir = script_dir / json_dir_path
    else:
        json_dir = json_dir_path

    if not json_dir.exists():
        print(f"错误：目录不存在 {json_dir}")
        return

    print(f"扫描目录：{json_dir}")

    # 统计不同类型的文件
    file_types = {
        'detail_comments': [],
        'search_comments': [],
        'detail_contents': [],
        'search_contents': [],
        'unknown': []
    }

    # 遍历目录下的所有JSON文件
    for json_file in json_dir.glob("*.json"):
        file_type = get_file_type(json_file.name)
        file_types[file_type].append(json_file)

    # 显示文件统计
    print("\n文件统计：")
    for file_type, files in file_types.items():
        if files:
            print(f"{file_type}: {len(files)} 个文件")
            for file in files:
                print(f"  - {file.name}")

    # 处理所有识别的文件
    total_processed = 0
    for file_type, files in file_types.items():
        if file_type != 'unknown' and files:
            print(f"\n开始处理 {file_type} 类型文件...")
            for json_file in files:
                extract_douyin_data(json_file)
                total_processed += 1

    if file_types['unknown']:
        print(f"\n跳过 {len(file_types['unknown'])} 个未识别类型的文件")

    print(f"\n处理完成！共处理了 {total_processed} 个文件")


if __name__ == "__main__":
    print("抖音数据提取脚本")
    print("=" * 50)
    print("支持的文件类型：")
    print("1. detail_comments_*.json - 详情页评论数据")
    print("2. search_comments_*.json - 搜索页评论数据")
    print("3. detail_contents_*.json - 详情页内容数据")
    print("4. search_contents_*.json - 搜索页内容数据")
    print("=" * 50)

    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    # 向上一级目录找到data文件夹
    json_dir = script_dir.parent / "data/douyin/json"

    main(json_dir)
