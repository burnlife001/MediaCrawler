#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL解析功能测试脚本
"""

import sys
import os

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from ui.controllers.url_parser import URLParser


def test_douyin_share_text():
    """测试抖音分享文本解析"""
    print("=" * 60)
    print("测试抖音分享文本解析")
    print("=" * 60)
    
    parser = URLParser()
    
    # 真实的抖音分享文本
    share_text = """6.48 F@h.Ok 10/25 MWM:/ 顶级杀手的食量就这么大吗 |《豺狼的日子》解说第五期 - 大家好，这里是《心中之城》。《豺狼的日子》第五期解说到此结束。第六期，将会是《豺狼的日子》解说最终期。我会尽快做出来。而如果有朋友愿意去欣赏原片，那当然很好。 - 在本期，我们知道了豺狼的过去。他是一个目睹了屠杀，然后屠杀了所有罪人的人。可我猜测，那场屠杀的回忆中，使豺狼永不能寐的，是他自己开的那一枪。他开枪消灭了远方山坡上，一个持枪瞄准他队友的威胁。结果，那人不是狙击手，那人拿的只是一支突击步枪。在那人倒地时，枪支走火，惊起了一群鸟，也惊动了紧张的队友和阿富汗人，导致了开火，然后，间接导致了屠杀。 - 豺狼不是一个心软之人。他开的那一枪，许多人会做出不同的选择，有些人会赌一把，赌对方不会开枪；有些人会立刻通知队友撤退；有些人会再确认一下，确认那人有没有射程条件。而豺狼只是很快地做出决定：清除威胁。至于对方会不会开枪，他不考虑。他是天生的杀手。 - 可是，在豺狼满不在乎地对努丽娅说出"我为钱杀人"的时候，努丽娅一下就看穿了他。她死死盯着他的眼睛，挺身直面，要他一遍、一遍，再说、再说、再说…… 真实的他，渐渐露出原型。 他的不在乎是装的，他的轻佻和冷漠都是装的。 真实的他，怒不可遏，恨入骨髓。 - 他恨世界太不公平，把他逼到如此境地，让他失去了所有救赎的可能；也恨自己，万业缠身，只能一错再错，一条道走到黑。他想要的活法，就是躲藏、逃避、遗忘，去很远的地方，去无人知晓的地方，永远不要回到过去。就像鸟儿一样。这是豺狼的梦。  https://v.douyin.com/ZBtP90iVSY8/ 复制此链接，打开Dou音搜索，直接观看视频！"""
    
    print("原始分享文本:")
    print(share_text[:200] + "..." if len(share_text) > 200 else share_text)
    print()
    
    # 测试URL提取
    extracted_url = parser.extract_url_from_text(share_text, "dy")
    print(f"提取的URL: {extracted_url}")
    
    # 测试验证
    is_valid, message = parser.validate_url(share_text, "dy")
    print(f"验证结果: {is_valid}")
    print(f"验证消息: {message}")
    
    # 测试解析
    if is_valid:
        result = parser.parse_url(share_text, "dy")
        print(f"解析结果: {result}")
    
    print()


def test_various_douyin_urls():
    """测试各种抖音URL格式"""
    print("=" * 60)
    print("测试各种抖音URL格式")
    print("=" * 60)
    
    parser = URLParser()
    
    test_urls = [
        "https://www.douyin.com/video/7502468477924560168",
        "https://v.douyin.com/ZBtP90iVSY8/",
        "https://v.douyin.com/ZBtP90iVSY8",
        "https://www.iesdouyin.com/share/video/7502468477924560168",
    ]
    
    for url in test_urls:
        print(f"测试URL: {url}")
        
        # 验证
        is_valid, message = parser.validate_url(url, "dy")
        print(f"  验证: {is_valid} - {message}")
        
        # 解析
        if is_valid:
            result = parser.parse_url(url, "dy")
            print(f"  解析: {result}")
        
        print()


def test_xiaohongshu_urls():
    """测试小红书URL格式"""
    print("=" * 60)
    print("测试小红书URL格式")
    print("=" * 60)
    
    parser = URLParser()
    
    test_urls = [
        "https://www.xiaohongshu.com/explore/64a1b2c3d4e5f6789012345a",
        "https://www.xiaohongshu.com/explore/64a1b2c3d4e5f6789012345a?xsec_token=xxx&xsec_source=pc_search",
        "https://xhslink.com/AbCdEf",
    ]
    
    for url in test_urls:
        print(f"测试URL: {url}")
        
        # 验证
        is_valid, message = parser.validate_url(url, "xhs")
        print(f"  验证: {is_valid} - {message}")
        
        # 解析
        if is_valid:
            result = parser.parse_url(url, "xhs")
            print(f"  解析: {result}")
        
        print()


def test_mixed_text():
    """测试包含URL的混合文本"""
    print("=" * 60)
    print("测试包含URL的混合文本")
    print("=" * 60)
    
    parser = URLParser()
    
    # 模拟小红书分享文本
    xhs_text = """
    今天分享一个超好用的护肤品！真的太爱了❤️
    效果超级棒，推荐给大家～
    
    https://www.xiaohongshu.com/explore/64a1b2c3d4e5f6789012345a?xsec_token=xxx&xsec_source=pc_search
    
    快来看看吧！
    """
    
    print("小红书混合文本:")
    print(xhs_text.strip())
    print()
    
    # 提取URL
    extracted_url = parser.extract_url_from_text(xhs_text, "xhs")
    print(f"提取的URL: {extracted_url}")
    
    # 验证和解析
    is_valid, message = parser.validate_url(xhs_text, "xhs")
    print(f"验证结果: {is_valid} - {message}")
    
    if is_valid:
        result = parser.parse_url(xhs_text, "xhs")
        print(f"解析结果: {result}")


def main():
    """主函数"""
    print("MediaCrawler URL解析功能测试")
    print("=" * 80)
    
    try:
        # 测试抖音分享文本
        test_douyin_share_text()
        
        # 测试各种抖音URL
        test_various_douyin_urls()
        
        # 测试小红书URL
        test_xiaohongshu_urls()
        
        # 测试混合文本
        test_mixed_text()
        
        print("=" * 80)
        print("所有URL解析测试完成！")
        
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
