#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL解析器
"""

import re
import urllib.parse
from typing import Optional, Dict, Tuple


class URLParser:
    """URL解析器类"""
    
    def __init__(self):
        # 抖音URL模式
        self.douyin_patterns = [
            r'https?://(?:www\.)?douyin\.com/video/(\d+)',  # 标准链接
            r'https?://v\.douyin\.com/[A-Za-z0-9]+/?',      # 短链接
            r'https?://(?:www\.)?iesdouyin\.com/share/video/(\d+)',  # 分享链接
        ]
        
        # 小红书URL模式
        self.xiaohongshu_patterns = [
            r'https?://(?:www\.)?xiaohongshu\.com/explore/([a-f0-9]+)',  # 标准链接
            r'https?://xhslink\.com/[A-Za-z0-9]+',  # 短链接
            r'http://xhslink\.com/[A-Za-z0-9]+',    # 短链接(http)
        ]
    
    def extract_url_from_text(self, text: str, platform: str) -> Optional[str]:
        """
        从文本中提取URL

        Args:
            text: 包含URL的文本
            platform: 平台类型

        Returns:
            提取的URL，失败返回None
        """
        if platform == "dy":
            # 抖音URL模式
            patterns = [
                r'https?://(?:www\.)?douyin\.com/video/\d+',
                r'https?://v\.douyin\.com/[A-Za-z0-9]+/?',
                r'https?://(?:www\.)?iesdouyin\.com/share/video/\d+',
            ]
        elif platform == "xhs":
            # 小红书URL模式
            patterns = [
                r'https?://(?:www\.)?xiaohongshu\.com/explore/[a-f0-9]+(?:\?[^\\s]*)?',
                r'https?://xhslink\.com/[A-Za-z0-9]+',
            ]
        else:
            return None

        # 尝试匹配所有模式
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)

        return None

    def validate_url(self, url: str, platform: str) -> Tuple[bool, str]:
        """
        验证URL格式

        Args:
            url: 要验证的URL或包含URL的文本
            platform: 平台类型 ('dy' 或 'xhs')

        Returns:
            (是否有效, 错误信息)
        """
        if not url or not url.strip():
            return False, "URL不能为空"

        text = url.strip()

        # 首先尝试从文本中提取URL
        extracted_url = self.extract_url_from_text(text, platform)
        if extracted_url:
            url = extracted_url
        else:
            # 如果没有提取到URL，检查原文本是否是有效URL
            try:
                parsed = urllib.parse.urlparse(text)
                if not parsed.scheme or not parsed.netloc:
                    return False, "未找到有效的URL链接"
                url = text
            except Exception:
                return False, "未找到有效的URL链接"

        if platform == "dy":
            return self._validate_douyin_url(url)
        elif platform == "xhs":
            return self._validate_xiaohongshu_url(url)
        else:
            return False, "不支持的平台"
    
    def _validate_douyin_url(self, url: str) -> Tuple[bool, str]:
        """验证抖音URL"""
        for pattern in self.douyin_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True, "URL格式正确"
        
        return False, "不是有效的抖音视频链接"
    
    def _validate_xiaohongshu_url(self, url: str) -> Tuple[bool, str]:
        """验证小红书URL"""
        for pattern in self.xiaohongshu_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True, "URL格式正确"
        
        return False, "不是有效的小红书笔记链接"
    
    def parse_url(self, url: str, platform: str) -> Optional[Dict[str, str]]:
        """
        解析URL，提取ID等信息

        Args:
            url: 要解析的URL或包含URL的文本
            platform: 平台类型 ('dy' 或 'xhs')

        Returns:
            解析结果字典，包含id等信息，失败返回None
        """
        if not url or not url.strip():
            return None

        text = url.strip()

        # 首先尝试从文本中提取URL
        extracted_url = self.extract_url_from_text(text, platform)
        if extracted_url:
            actual_url = extracted_url
            original_text = text
        else:
            actual_url = text
            original_text = text

        if platform == "dy":
            result = self._parse_douyin_url(actual_url)
        elif platform == "xhs":
            result = self._parse_xiaohongshu_url(actual_url)
        else:
            return None

        # 如果解析成功且原文本不是纯URL，记录原始文本
        if result and extracted_url and len(original_text) > len(extracted_url) + 10:
            result["original_text"] = original_text
            result["extracted_url"] = extracted_url

        return result
    
    def _parse_douyin_url(self, url: str) -> Optional[Dict[str, str]]:
        """解析抖音URL"""
        # 尝试从标准链接提取ID
        match = re.search(r'douyin\.com/video/(\d+)', url, re.IGNORECASE)
        if match:
            aweme_id = match.group(1)
            return {
                "id": aweme_id,
                "platform": "dy",
                "type": "video",
                "original_url": url,
                "parsed_url": url
            }

        # 处理短链接 - 直接使用，浏览器会自动重定向
        if re.search(r'v\.douyin\.com', url, re.IGNORECASE):
            return {
                "id": "short_link",  # 标记为短链接
                "platform": "dy",
                "type": "video",
                "original_url": url,
                "parsed_url": url,
                "is_short_link": True
            }

        # 处理分享链接
        match = re.search(r'iesdouyin\.com/share/video/(\d+)', url, re.IGNORECASE)
        if match:
            aweme_id = match.group(1)
            return {
                "id": aweme_id,
                "platform": "dy",
                "type": "video",
                "original_url": url,
                "parsed_url": url
            }

        return None
    
    def _parse_xiaohongshu_url(self, url: str) -> Optional[Dict[str, str]]:
        """解析小红书URL"""
        # 尝试从标准链接提取ID
        match = re.search(r'xiaohongshu\.com/explore/([a-f0-9]+)', url, re.IGNORECASE)
        if match:
            note_id = match.group(1)
            
            # 提取URL参数
            parsed_url = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed_url.query)
            
            result = {
                "id": note_id,
                "platform": "xhs",
                "type": "note",
                "original_url": url,
                "parsed_url": f"https://www.xiaohongshu.com/explore/{note_id}"
            }
            
            # 提取xsec_token和xsec_source参数（小红书API需要）
            if "xsec_token" in params:
                result["xsec_token"] = params["xsec_token"][0]
            if "xsec_source" in params:
                result["xsec_source"] = params["xsec_source"][0]
            
            return result
        
        # 处理短链接
        if re.search(r'xhslink\.com', url, re.IGNORECASE):
            return {
                "id": "unknown",  # 短链接需要重定向才能获取真实ID
                "platform": "xhs",
                "type": "note", 
                "original_url": url,
                "parsed_url": url,
                "needs_redirect": True
            }
        
        return None
    
    def extract_id_from_url(self, url: str, platform: str) -> Optional[str]:
        """
        从URL中提取ID
        
        Args:
            url: URL字符串
            platform: 平台类型
            
        Returns:
            提取的ID，失败返回None
        """
        result = self.parse_url(url, platform)
        return result.get("id") if result else None
    
    def is_short_url(self, url: str, platform: str) -> bool:
        """
        判断是否是短链接
        
        Args:
            url: URL字符串
            platform: 平台类型
            
        Returns:
            是否是短链接
        """
        if platform == "dy":
            return bool(re.search(r'v\.douyin\.com', url, re.IGNORECASE))
        elif platform == "xhs":
            return bool(re.search(r'xhslink\.com', url, re.IGNORECASE))
        return False
    
    def normalize_url(self, url: str, platform: str) -> Optional[str]:
        """
        标准化URL
        
        Args:
            url: 原始URL
            platform: 平台类型
            
        Returns:
            标准化后的URL
        """
        result = self.parse_url(url, platform)
        if result and not result.get("needs_redirect"):
            return result.get("parsed_url")
        return url
    
    def get_supported_platforms(self) -> Dict[str, str]:
        """获取支持的平台列表"""
        return {
            "dy": "抖音",
            "xhs": "小红书"
        }
    
    def get_platform_examples(self, platform: str) -> list:
        """获取平台URL示例"""
        examples = {
            "dy": [
                "https://www.douyin.com/video/7234567890123456789",
                "https://v.douyin.com/AbCdEfG/",
                "https://www.iesdouyin.com/share/video/7234567890123456789"
            ],
            "xhs": [
                "https://www.xiaohongshu.com/explore/64a1b2c3d4e5f6789012345a",
                "https://xhslink.com/AbCdEf",
                "https://www.xiaohongshu.com/explore/64a1b2c3d4e5f6789012345a?xsec_token=xxx&xsec_source=pc_search"
            ]
        }
        return examples.get(platform, [])

    async def resolve_short_url(self, url: str) -> Optional[str]:
        """
        解析短链接获取真实URL

        Args:
            url: 短链接

        Returns:
            真实URL，失败返回None
        """
        try:
            import httpx

            async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
                response = await client.head(url)
                return str(response.url)

        except Exception as e:
            logging.error(f"解析短链接失败: {url}, 错误: {str(e)}")
            return None

    async def parse_url_with_redirect(self, url: str, platform: str) -> Optional[Dict[str, str]]:
        """
        解析URL，如果是短链接则先解析重定向

        Args:
            url: 要解析的URL
            platform: 平台类型

        Returns:
            解析结果
        """
        # 首先尝试直接解析
        result = self.parse_url(url, platform)

        # 如果是短链接，尝试解析重定向
        if result and result.get("needs_redirect"):
            real_url = await self.resolve_short_url(url)
            if real_url:
                # 用真实URL重新解析
                result = self.parse_url(real_url, platform)
                if result:
                    result["original_url"] = url
                    result["resolved_url"] = real_url

        return result
