#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler UI 综合测试脚本
"""

import sys
import os

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

def test_dependencies():
    """测试依赖"""
    print("=" * 60)
    print("测试依赖")
    print("=" * 60)
    
    try:
        from ui.utils.dependency_checker import DependencyChecker
        
        checker = DependencyChecker()
        deps_ok, missing_packages, error_messages = checker.check_all_dependencies()
        
        if deps_ok:
            print("✅ 所有依赖检查通过")
        else:
            print(f"❌ 发现 {len(missing_packages)} 个缺失的依赖包:")
            for pkg in missing_packages:
                print(f"  - {pkg}")
        
        return deps_ok
        
    except Exception as e:
        print(f"❌ 依赖测试失败: {str(e)}")
        return False

def test_url_parsing():
    """测试URL解析"""
    print("\n" + "=" * 60)
    print("测试URL解析")
    print("=" * 60)
    
    try:
        from ui.controllers.url_parser import URLParser
        
        parser = URLParser()
        
        # 测试抖音分享文本
        share_text = """6.48 F@h.Ok 10/25 MWM:/ 顶级杀手的食量就这么大吗 |《豺狼的日子》解说第五期 - 大家好，这里是《心中之城》。《豺狼的日子》第五期解说到此结束。第六期，将会是《豺狼的日子》解说最终期。我会尽快做出来。而如果有朋友愿意去欣赏原片，那当然很好。 - 在本期，我们知道了豺狼的过去。他是一个目睹了屠杀，然后屠杀了所有罪人的人。可我猜测，那场屠杀的回忆中，使豺狼永不能寐的，是他自己开的那一枪。他开枪消灭了远方山坡上，一个持枪瞄准他队友的威胁。结果，那人不是狙击手，那人拿的只是一支突击步枪。在那人倒地时，枪支走火，惊起了一群鸟，也惊动了紧张的队友和阿富汗人，导致了开火，然后，间接导致了屠杀。 - 豺狼不是一个心软之人。他开的那一枪，许多人会做出不同的选择，有些人会赌一把，赌对方不会开枪；有些人会立刻通知队友撤退；有些人会再确认一下，确认那人有没有射程条件。而豺狼只是很快地做出决定：清除威胁。至于对方会不会开枪，他不考虑。他是天生的杀手。 - 可是，在豺狼满不在乎地对努丽娅说出"我为钱杀人"的时候，努丽娅一下就看穿了他。她死死盯着他的眼睛，挺身直面，要他一遍、一遍，再说、再说、再说…… 真实的他，渐渐露出原型。 他的不在乎是装的，他的轻佻和冷漠都是装的。 真实的他，怒不可遏，恨入骨髓。 - 他恨世界太不公平，把他逼到如此境地，让他失去了所有救赎的可能；也恨自己，万业缠身，只能一错再错，一条道走到黑。他想要的活法，就是躲藏、逃避、遗忘，去很远的地方，去无人知晓的地方，永远不要回到过去。就像鸟儿一样。这是豺狼的梦。  https://v.douyin.com/ZBtP90iVSY8/ 复制此链接，打开Dou音搜索，直接观看视频！"""
        
        # 验证URL提取
        extracted_url = parser.extract_url_from_text(share_text, "dy")
        print(f"提取的URL: {extracted_url}")
        
        if extracted_url == "https://v.douyin.com/ZBtP90iVSY8/":
            print("✅ URL提取功能正常")
            
            # 验证URL解析
            result = parser.parse_url(share_text, "dy")
            if result and result.get('extracted_url') == extracted_url:
                print("✅ URL解析功能正常")
                return True
            else:
                print("❌ URL解析功能异常")
                return False
        else:
            print("❌ URL提取功能异常")
            return False
        
    except Exception as e:
        print(f"❌ URL解析测试失败: {str(e)}")
        return False

def test_data_processing():
    """测试数据处理"""
    print("\n" + "=" * 60)
    print("测试数据处理")
    print("=" * 60)
    
    try:
        from ui.controllers.data_processor import DataProcessor
        
        processor = DataProcessor()
        
        # 测试数据添加
        test_data = {
            "nickname": "测试用户",
            "content": "测试评论",
            "aweme_url": "https://www.douyin.com/video/123456789",
            "home_url": "https://www.douyin.com/user/test",
        }
        
        processor.add_data(test_data)
        
        if processor.get_data_count() == 1:
            print("✅ 数据添加功能正常")
            
            # 测试导出
            try:
                file_path = processor.export_to_excel("test_export.xlsx")
                if os.path.exists(file_path):
                    print("✅ 数据导出功能正常")
                    os.remove(file_path)  # 清理测试文件
                    return True
                else:
                    print("❌ 导出文件不存在")
                    return False
            except Exception as e:
                print(f"❌ 数据导出失败: {str(e)}")
                return False
        else:
            print("❌ 数据添加功能异常")
            return False
        
    except Exception as e:
        print(f"❌ 数据处理测试失败: {str(e)}")
        return False

def test_config_management():
    """测试配置管理"""
    print("\n" + "=" * 60)
    print("测试配置管理")
    print("=" * 60)
    
    try:
        from ui.utils.config_manager import ConfigManager
        
        config_manager = ConfigManager()
        config = config_manager.get_config()
        
        # 检查默认配置
        if config.get('platform') == 'dy':
            print("✅ 默认平台配置正确")
            
            # 测试配置保存
            test_config = {'test_key': 'test_value'}
            success = config_manager.update_config(test_config)
            
            if success:
                print("✅ 配置保存功能正常")
                return True
            else:
                print("❌ 配置保存功能异常")
                return False
        else:
            print("❌ 默认平台配置错误")
            return False
        
    except Exception as e:
        print(f"❌ 配置管理测试失败: {str(e)}")
        return False

def test_ui_components():
    """测试UI组件导入"""
    print("\n" + "=" * 60)
    print("测试UI组件导入")
    print("=" * 60)
    
    ui_modules = [
        'ui.utils.config_manager',
        'ui.utils.dependency_checker',
        'ui.controllers.url_parser',
        'ui.controllers.data_processor',
        'ui.components.config_panel',
        'ui.components.progress_panel',
        'ui.components.result_panel',
        'ui.main_window',
        'ui.app'
    ]
    
    success_count = 0
    total_count = len(ui_modules)
    
    for module_name in ui_modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module_name} (导入失败: {str(e)})")
        except Exception as e:
            print(f"⚠ {module_name} (错误: {str(e)})")
    
    print(f"\nUI组件导入测试结果: {success_count}/{total_count} 成功")
    return success_count == total_count

def main():
    """主函数"""
    print("MediaCrawler UI 综合测试")
    print("=" * 80)
    
    try:
        # 运行所有测试
        deps_ok = test_dependencies()
        url_ok = test_url_parsing()
        data_ok = test_data_processing()
        config_ok = test_config_management()
        ui_ok = test_ui_components()
        
        print("\n" + "=" * 80)
        print("测试总结:")
        print(f"  依赖检查:   {'✅' if deps_ok else '❌'}")
        print(f"  URL解析:    {'✅' if url_ok else '❌'}")
        print(f"  数据处理:   {'✅' if data_ok else '❌'}")
        print(f"  配置管理:   {'✅' if config_ok else '❌'}")
        print(f"  UI组件:     {'✅' if ui_ok else '❌'}")
        
        all_passed = all([deps_ok, url_ok, data_ok, config_ok, ui_ok])
        
        if all_passed:
            print("\n🎉 所有测试通过！MediaCrawler UI 可以正常使用")
            return True
        else:
            print("\n❌ 部分测试失败，请检查相关功能")
            return False
        
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
