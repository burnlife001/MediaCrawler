#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理器
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path


class DataProcessor:
    """数据处理器类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 数据缓冲区
        self.data_buffer: List[Dict[str, Any]] = []
        
        # 导出设置
        self.auto_export_threshold = 10  # 降低阈值便于测试
        self.export_format = "xlsx"
        self.export_counter = 0
        
        # 数据统计
        self.total_processed = 0
        self.last_export_time = None

        # 当前会话的导出文件路径
        self.current_session_file = None
        self.session_exported_count = 0

        # 输出目录
        self.output_dir = self._get_output_dir()
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _get_output_dir(self) -> str:
        """获取输出目录"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        return os.path.join(project_root, "data", "ui_exports")
    
    def add_data(self, data: Dict[str, Any]):
        """添加单条数据"""
        try:
            # 格式化数据
            formatted_data = self._format_data(data)
            
            # 添加到缓冲区
            self.data_buffer.append(formatted_data)
            self.total_processed += 1
            
            self.logger.debug(f"添加数据: {formatted_data.get('nickname', 'Unknown')}")
            
        except Exception as e:
            self.logger.error(f"添加数据失败: {str(e)}")
    
    def add_batch_data(self, data_list: List[Dict[str, Any]]):
        """批量添加数据"""
        for data in data_list:
            self.add_data(data)
    
    def _format_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """格式化数据"""
        # 标准化字段名
        formatted = {
            "nickname": data.get("nickname", ""),
            "content": data.get("content", ""),
            "aweme_url": data.get("aweme_url", ""),
            "home_url": data.get("home_url", ""),
            "user_id": data.get("user_id", ""),
            "title": data.get("title", ""),
            "video_download_url": data.get("video_download_url", ""),
            "create_time": data.get("create_time", ""),
            "like_count": data.get("like_count", 0),
            "reply_count": data.get("reply_count", 0),
            "processed_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 清理数据
        for key, value in formatted.items():
            if isinstance(value, str):
                formatted[key] = value.strip()
            elif value is None:
                formatted[key] = ""
        
        return formatted
    
    def should_auto_export(self) -> bool:
        """检查是否应该自动导出"""
        return len(self.data_buffer) >= 100  # 固定100条触发自动导出
    
    def auto_export(self) -> Optional[str]:
        """自动导出数据"""
        if not self.data_buffer:
            return None

        try:
            # 如果是第一次导出，创建新文件
            if self.current_session_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"crawl_result_{timestamp}.{self.export_format}"
                self.current_session_file = os.path.join(self.output_dir, filename)

            # 导出数据到当前会话文件
            self._append_to_session_file(self.data_buffer)

            # 清空缓冲区
            exported_count = len(self.data_buffer)
            self.session_exported_count += exported_count
            self.data_buffer.clear()

            self.last_export_time = datetime.now()
            self.logger.info(f"自动导出完成: {self.current_session_file}, 本次导出 {exported_count} 条，累计 {self.session_exported_count} 条")

            return self.current_session_file

        except Exception as e:
            self.logger.error(f"自动导出失败: {str(e)}")
            raise
    
    def export_to_excel(self, filename: Optional[str] = None) -> Optional[str]:
        """导出到Excel文件"""
        if not self.data_buffer:
            return None
        
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"manual_export_{timestamp}.xlsx"
            
            return self._export_data(self.data_buffer, filename)
            
        except Exception as e:
            self.logger.error(f"导出Excel失败: {str(e)}")
            raise
    
    def export_to_csv(self, filename: Optional[str] = None) -> Optional[str]:
        """导出到CSV文件"""
        if not self.data_buffer:
            return None
        
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"manual_export_{timestamp}.csv"
            
            return self._export_data(self.data_buffer, filename, format_type="csv")
            
        except Exception as e:
            self.logger.error(f"导出CSV失败: {str(e)}")
            raise
    
    def export_to_json(self, filename: Optional[str] = None) -> Optional[str]:
        """导出到JSON文件"""
        if not self.data_buffer:
            return None
        
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"manual_export_{timestamp}.json"
            
            return self._export_data(self.data_buffer, filename, format_type="json")
            
        except Exception as e:
            self.logger.error(f"导出JSON失败: {str(e)}")
            raise
    
    def _export_data(self, data: List[Dict[str, Any]], filename: str, 
                    format_type: Optional[str] = None) -> str:
        """导出数据到文件"""
        file_path = os.path.join(self.output_dir, filename)
        
        # 根据文件扩展名或指定格式确定导出类型
        if format_type is None:
            format_type = Path(filename).suffix.lower().lstrip('.')
        
        if format_type == "xlsx":
            self._export_to_excel_file(data, file_path)
        elif format_type == "csv":
            self._export_to_csv_file(data, file_path)
        elif format_type == "json":
            self._export_to_json_file(data, file_path)
        else:
            raise ValueError(f"不支持的导出格式: {format_type}")
        
        return file_path
    
    def _export_to_excel_file(self, data: List[Dict[str, Any]], file_path: str):
        """导出到Excel文件"""
        df = pd.DataFrame(data)
        
        # 重新排列列的顺序
        columns_order = [
            "nickname", "content", "aweme_url", "home_url", 
            "user_id", "title", "video_download_url", 
            "create_time", "like_count", "reply_count", "processed_time"
        ]
        
        # 只保留存在的列
        existing_columns = [col for col in columns_order if col in df.columns]
        df = df[existing_columns]
        
        # 设置列名
        column_names = {
            "nickname": "昵称",
            "content": "评论内容",
            "aweme_url": "视频链接", 
            "home_url": "用户主页",
            "user_id": "用户ID",
            "title": "视频标题",
            "video_download_url": "视频下载链接",
            "create_time": "创建时间",
            "like_count": "点赞数",
            "reply_count": "回复数",
            "processed_time": "处理时间"
        }
        
        df.rename(columns=column_names, inplace=True)
        
        # 导出到Excel
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='评论数据')
            
            # 调整列宽
            worksheet = writer.sheets['评论数据']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)  # 最大宽度50
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    def _export_to_csv_file(self, data: List[Dict[str, Any]], file_path: str):
        """导出到CSV文件"""
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False, encoding='utf-8-sig')  # 使用utf-8-sig支持中文
    
    def _export_to_json_file(self, data: List[Dict[str, Any]], file_path: str):
        """导出到JSON文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_data_count(self) -> int:
        """获取当前数据数量"""
        return len(self.data_buffer)
    
    def get_total_processed(self) -> int:
        """获取总处理数量"""
        return self.total_processed
    
    def clear(self):
        """清空数据"""
        self.data_buffer.clear()
        self.logger.info("数据缓冲区已清空")
    
    def reset(self):
        """重置处理器"""
        self.data_buffer.clear()
        self.total_processed = 0
        self.export_counter = 0
        self.last_export_time = None
        self.current_session_file = None
        self.session_exported_count = 0
        self.logger.info("数据处理器已重置")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "buffer_count": len(self.data_buffer),
            "total_processed": self.total_processed,
            "export_counter": self.export_counter,
            "last_export_time": self.last_export_time.strftime("%Y-%m-%d %H:%M:%S") if self.last_export_time else None,
            "auto_export_threshold": self.auto_export_threshold
        }
    
    def set_auto_export_threshold(self, threshold: int):
        """设置自动导出阈值"""
        if threshold > 0:
            self.auto_export_threshold = threshold
            self.logger.info(f"自动导出阈值设置为: {threshold}")
    
    def set_export_format(self, format_type: str):
        """设置导出格式"""
        if format_type in ["xlsx", "csv", "json"]:
            self.export_format = format_type
            self.logger.info(f"导出格式设置为: {format_type}")
    
    def get_recent_data(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取最近的数据"""
        return self.data_buffer[-count:] if len(self.data_buffer) >= count else self.data_buffer.copy()

    def finish_session_export(self) -> Optional[str]:
        """结束会话时的导出"""
        if not self.data_buffer:
            return self.current_session_file

        try:
            # 如果还有未导出的数据，导出到当前会话文件
            if self.current_session_file is None:
                # 如果没有会话文件，创建新文件
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"crawl_result_{timestamp}.{self.export_format}"
                self.current_session_file = os.path.join(self.output_dir, filename)

            # 导出剩余数据
            self._append_to_session_file(self.data_buffer)

            exported_count = len(self.data_buffer)
            self.session_exported_count += exported_count
            self.data_buffer.clear()

            self.logger.info(f"会话结束导出: {self.current_session_file}, 本次导出 {exported_count} 条，总计 {self.session_exported_count} 条")

            return self.current_session_file

        except Exception as e:
            self.logger.error(f"会话结束导出失败: {str(e)}")
            raise

    def _append_to_session_file(self, data: List[Dict[str, Any]]):
        """追加数据到会话文件"""
        if not data:
            return

        # 如果文件不存在，创建新文件
        if not os.path.exists(self.current_session_file):
            self._export_to_excel_file(data, self.current_session_file)
        else:
            # 文件存在，追加数据
            self._append_to_excel_file(data, self.current_session_file)

    def _append_to_excel_file(self, data: List[Dict[str, Any]], file_path: str):
        """追加数据到Excel文件"""
        import pandas as pd
        from openpyxl import load_workbook

        # 读取现有数据
        existing_df = pd.read_excel(file_path, sheet_name='评论数据')

        # 格式化新数据
        new_df = pd.DataFrame(data)

        # 重新排列列的顺序
        columns_order = [
            "nickname", "content", "aweme_url", "home_url",
            "user_id", "title", "video_download_url",
            "create_time", "like_count", "reply_count", "processed_time"
        ]

        # 只保留存在的列
        existing_columns = [col for col in columns_order if col in new_df.columns]
        new_df = new_df[existing_columns]

        # 设置列名
        column_names = {
            "nickname": "昵称",
            "content": "评论内容",
            "aweme_url": "视频链接",
            "home_url": "用户主页",
            "user_id": "用户ID",
            "title": "视频标题",
            "video_download_url": "视频下载链接",
            "create_time": "创建时间",
            "like_count": "点赞数",
            "reply_count": "回复数",
            "processed_time": "处理时间"
        }

        new_df.rename(columns=column_names, inplace=True)

        # 合并数据
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)

        # 重新写入文件
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            combined_df.to_excel(writer, index=False, sheet_name='评论数据')

            # 调整列宽
            worksheet = writer.sheets['评论数据']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)  # 最大宽度50
                worksheet.column_dimensions[column_letter].width = adjusted_width
