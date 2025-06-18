#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结果面板组件
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any
import webbrowser


class ResultPanel:
    """结果面板类"""
    
    def __init__(self, parent):
        self.parent = parent
        self.data_list: List[Dict[str, Any]] = []
        
        # 创建UI
        self._create_widgets()
        self._setup_context_menu()
    
    def _create_widgets(self):
        """创建结果面板UI"""
        # 主框架
        self.frame = ttk.LabelFrame(self.parent, text="结果预览", padding="5")
        
        # 创建Treeview表格
        columns = ("nickname", "content", "aweme_url", "home_url", "time")
        column_names = ("昵称", "评论内容", "视频链接", "用户主页", "时间")
        
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=12)
        
        # 设置列标题和宽度
        for col, name in zip(columns, column_names):
            self.tree.heading(col, text=name, command=lambda c=col: self._sort_column(c))
            if col == "content":
                self.tree.column(col, width=300, minwidth=200)
            elif col == "nickname":
                self.tree.column(col, width=120, minwidth=80)
            elif col == "time":
                self.tree.column(col, width=120, minwidth=100)
            else:
                self.tree.column(col, width=150, minwidth=100)
        
        # 创建滚动条
        v_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 布局
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 配置网格权重
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # 状态栏
        status_frame = ttk.Frame(self.frame)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.status_label = ttk.Label(status_frame, text="共 0 条记录")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # 绑定事件
        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<Button-3>", self._on_right_click)  # 右键菜单
        
        # 排序相关变量
        self.sort_column = None
        self.sort_reverse = False
    
    def _setup_context_menu(self):
        """设置右键菜单"""
        self.context_menu = tk.Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="复制内容", command=self._copy_content)
        self.context_menu.add_command(label="复制链接", command=self._copy_link)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="打开视频链接", command=self._open_video_link)
        self.context_menu.add_command(label="打开用户主页", command=self._open_user_home)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="删除此条", command=self._delete_selected)
    
    def add_data(self, data: Dict[str, Any]):
        """添加单条数据"""
        # 格式化数据
        formatted_data = self._format_data(data)
        
        # 添加到数据列表
        self.data_list.append(formatted_data)
        
        # 添加到表格
        values = (
            formatted_data.get("nickname", ""),
            self._truncate_text(formatted_data.get("content", ""), 50),
            formatted_data.get("aweme_url", ""),
            formatted_data.get("home_url", ""),
            formatted_data.get("time", "")
        )
        
        item_id = self.tree.insert("", "end", values=values)
        
        # 滚动到最新添加的项
        self.tree.see(item_id)
        
        # 更新状态
        self._update_status()
    
    def add_batch_data(self, data_list: List[Dict[str, Any]]):
        """批量添加数据"""
        for data in data_list:
            self.add_data(data)
    
    def _format_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """格式化数据"""
        from datetime import datetime
        
        formatted = {
            "nickname": data.get("nickname", ""),
            "content": data.get("content", ""),
            "aweme_url": data.get("aweme_url", ""),
            "home_url": data.get("home_url", ""),
            "time": data.get("time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }
        
        # 清理和验证数据
        for key, value in formatted.items():
            if isinstance(value, str):
                formatted[key] = value.strip()
        
        return formatted
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """截断文本"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
    
    def _sort_column(self, col: str):
        """排序列"""
        # 如果点击的是同一列，则反转排序
        if self.sort_column == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False
        
        # 获取所有数据
        data = []
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            data.append((values, item))
        
        # 排序
        col_index = ("nickname", "content", "aweme_url", "home_url", "time").index(col)
        data.sort(key=lambda x: x[0][col_index], reverse=self.sort_reverse)
        
        # 重新插入数据
        for index, (values, item) in enumerate(data):
            self.tree.move(item, "", index)
        
        # 更新列标题显示排序状态
        for column in ("nickname", "content", "aweme_url", "home_url", "time"):
            if column == col:
                direction = " ↓" if self.sort_reverse else " ↑"
                self.tree.heading(column, text=self._get_column_name(column) + direction)
            else:
                self.tree.heading(column, text=self._get_column_name(column))
    
    def _get_column_name(self, col: str) -> str:
        """获取列的显示名称"""
        name_map = {
            "nickname": "昵称",
            "content": "评论内容", 
            "aweme_url": "视频链接",
            "home_url": "用户主页",
            "time": "时间"
        }
        return name_map.get(col, col)
    
    def _on_double_click(self, event):
        """双击事件处理"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            # 显示完整内容
            values = self.tree.item(item)["values"]
            content = self._get_full_content(item)
            self._show_detail_dialog(values, content)
    
    def _on_right_click(self, event):
        """右键点击事件处理"""
        # 选中右键点击的项
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def _get_full_content(self, item) -> str:
        """获取完整内容"""
        # 从原始数据中获取完整内容
        index = self.tree.index(item)
        if 0 <= index < len(self.data_list):
            return self.data_list[index].get("content", "")
        return ""
    
    def _show_detail_dialog(self, values, full_content):
        """显示详细信息对话框"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("详细信息")
        dialog.geometry("600x400")
        dialog.resizable(True, True)
        
        # 创建文本框显示完整内容
        text_frame = ttk.Frame(dialog, padding="10")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # 昵称
        ttk.Label(text_frame, text=f"昵称: {values[0]}", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # 内容
        ttk.Label(text_frame, text="评论内容:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        content_text = tk.Text(text_frame, wrap=tk.WORD, height=10, font=("Arial", 10))
        content_text.insert("1.0", full_content)
        content_text.config(state="disabled")
        content_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # 链接信息
        if values[2]:  # 视频链接
            ttk.Label(text_frame, text=f"视频链接: {values[2]}", font=("Arial", 9)).pack(anchor=tk.W, pady=(0, 5))
        if values[3]:  # 用户主页
            ttk.Label(text_frame, text=f"用户主页: {values[3]}", font=("Arial", 9)).pack(anchor=tk.W, pady=(0, 5))
        
        # 时间
        ttk.Label(text_frame, text=f"时间: {values[4]}", font=("Arial", 9)).pack(anchor=tk.W)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="关闭", command=dialog.destroy).pack(side=tk.RIGHT)
        if values[2]:
            ttk.Button(button_frame, text="打开视频", 
                      command=lambda: webbrowser.open(values[2])).pack(side=tk.RIGHT, padx=(0, 10))
    
    def _copy_content(self):
        """复制内容到剪贴板"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            content = self._get_full_content(item)
            self.frame.clipboard_clear()
            self.frame.clipboard_append(content)
            messagebox.showinfo("提示", "内容已复制到剪贴板")
    
    def _copy_link(self):
        """复制链接到剪贴板"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            values = self.tree.item(item)["values"]
            link = values[2] if values[2] else values[3]  # 优先视频链接，其次用户主页
            if link:
                self.frame.clipboard_clear()
                self.frame.clipboard_append(link)
                messagebox.showinfo("提示", "链接已复制到剪贴板")
            else:
                messagebox.showwarning("警告", "该条记录没有可用链接")
    
    def _open_video_link(self):
        """打开视频链接"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            values = self.tree.item(item)["values"]
            if values[2]:
                webbrowser.open(values[2])
            else:
                messagebox.showwarning("警告", "该条记录没有视频链接")
    
    def _open_user_home(self):
        """打开用户主页"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            values = self.tree.item(item)["values"]
            if values[3]:
                webbrowser.open(values[3])
            else:
                messagebox.showwarning("警告", "该条记录没有用户主页链接")
    
    def _delete_selected(self):
        """删除选中的记录"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            if messagebox.askyesno("确认", "确定要删除这条记录吗？"):
                # 从数据列表中删除
                index = self.tree.index(item)
                if 0 <= index < len(self.data_list):
                    del self.data_list[index]
                
                # 从表格中删除
                self.tree.delete(item)
                
                # 更新状态
                self._update_status()
    
    def _update_status(self):
        """更新状态栏"""
        count = len(self.data_list)
        self.status_label.config(text=f"共 {count} 条记录")
    
    def clear(self):
        """清空所有数据"""
        self.data_list.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._update_status()
    
    def get_data(self) -> List[Dict[str, Any]]:
        """获取所有数据"""
        return self.data_list.copy()
    
    def export_selected(self) -> List[Dict[str, Any]]:
        """导出选中的数据"""
        selected_items = self.tree.selection()
        if not selected_items:
            return []
        
        selected_data = []
        for item in selected_items:
            index = self.tree.index(item)
            if 0 <= index < len(self.data_list):
                selected_data.append(self.data_list[index])
        
        return selected_data
