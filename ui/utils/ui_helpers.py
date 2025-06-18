#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI辅助函数
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import asyncio
from typing import Callable, Any, Optional
import logging


def run_async_in_thread(async_func: Callable, *args, **kwargs):
    """在新线程中运行异步函数"""
    def run():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(async_func(*args, **kwargs))
        except Exception as e:
            logging.error(f"异步函数执行失败: {str(e)}")
        finally:
            loop.close()
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread


def center_window(window: tk.Tk, width: int, height: int):
    """将窗口居中显示"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")


def show_error_dialog(parent: tk.Widget, title: str, message: str):
    """显示错误对话框"""
    messagebox.showerror(title, message, parent=parent)


def show_warning_dialog(parent: tk.Widget, title: str, message: str):
    """显示警告对话框"""
    messagebox.showwarning(title, message, parent=parent)


def show_info_dialog(parent: tk.Widget, title: str, message: str):
    """显示信息对话框"""
    messagebox.showinfo(title, message, parent=parent)


def ask_yes_no(parent: tk.Widget, title: str, message: str) -> bool:
    """显示是/否确认对话框"""
    return messagebox.askyesno(title, message, parent=parent)


def select_file(parent: tk.Widget, title: str = "选择文件", 
               filetypes: list = None) -> Optional[str]:
    """选择文件对话框"""
    if filetypes is None:
        filetypes = [("所有文件", "*.*")]
    
    return filedialog.askopenfilename(
        parent=parent,
        title=title,
        filetypes=filetypes
    )


def select_directory(parent: tk.Widget, title: str = "选择目录") -> Optional[str]:
    """选择目录对话框"""
    return filedialog.askdirectory(parent=parent, title=title)


def save_file(parent: tk.Widget, title: str = "保存文件", 
             defaultextension: str = ".txt",
             filetypes: list = None) -> Optional[str]:
    """保存文件对话框"""
    if filetypes is None:
        filetypes = [("文本文件", "*.txt"), ("所有文件", "*.*")]
    
    return filedialog.asksaveasfilename(
        parent=parent,
        title=title,
        defaultextension=defaultextension,
        filetypes=filetypes
    )


def create_tooltip(widget: tk.Widget, text: str):
    """为控件创建工具提示"""
    def on_enter(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        
        label = tk.Label(tooltip, text=text, background="lightyellow", 
                        relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack()
        
        widget.tooltip = tooltip
    
    def on_leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            del widget.tooltip
    
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def validate_number_input(value: str, min_val: float = None, 
                         max_val: float = None, allow_float: bool = True) -> bool:
    """验证数字输入"""
    if not value:
        return True  # 允许空值
    
    try:
        if allow_float:
            num = float(value)
        else:
            num = int(value)
        
        if min_val is not None and num < min_val:
            return False
        if max_val is not None and num > max_val:
            return False
        
        return True
    except ValueError:
        return False


def create_scrollable_frame(parent: tk.Widget) -> tuple[tk.Frame, tk.Canvas, ttk.Scrollbar]:
    """创建可滚动的框架"""
    # 创建Canvas和Scrollbar
    canvas = tk.Canvas(parent)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    # 配置滚动
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    return scrollable_frame, canvas, scrollbar


def bind_mousewheel(widget: tk.Widget, canvas: tk.Canvas):
    """绑定鼠标滚轮事件"""
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def bind_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def unbind_from_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")
    
    widget.bind('<Enter>', bind_to_mousewheel)
    widget.bind('<Leave>', unbind_from_mousewheel)


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def format_duration(seconds: int) -> str:
    """格式化时间长度"""
    if seconds < 60:
        return f"{seconds}秒"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}分{secs}秒"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}时{minutes}分"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def safe_call(func: Callable, *args, **kwargs) -> Any:
    """安全调用函数，捕获异常"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logging.error(f"函数调用失败: {func.__name__}, 错误: {str(e)}")
        return None


class ProgressDialog:
    """进度对话框"""
    
    def __init__(self, parent: tk.Widget, title: str = "处理中..."):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        center_window(self.dialog, 400, 150)
        
        # 创建UI
        self._create_widgets()
        
        # 变量
        self.cancelled = False
    
    def _create_widgets(self):
        """创建UI组件"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, text="正在处理...")
        self.status_label.pack(pady=(0, 10))
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=300)
        self.progress_bar.pack(pady=(0, 10))
        
        # 进度文本
        self.progress_label = ttk.Label(main_frame, text="0%")
        self.progress_label.pack(pady=(0, 10))
        
        # 取消按钮
        self.cancel_button = ttk.Button(main_frame, text="取消", 
                                       command=self._on_cancel)
        self.cancel_button.pack()
    
    def update_progress(self, percentage: float, status: str = None):
        """更新进度"""
        self.progress_var.set(percentage)
        self.progress_label.config(text=f"{percentage:.1f}%")
        
        if status:
            self.status_label.config(text=status)
        
        self.dialog.update()
    
    def _on_cancel(self):
        """取消按钮点击"""
        self.cancelled = True
        self.close()
    
    def is_cancelled(self) -> bool:
        """检查是否被取消"""
        return self.cancelled
    
    def close(self):
        """关闭对话框"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None


def create_loading_dialog(parent: tk.Widget, message: str = "加载中...") -> tk.Toplevel:
    """创建加载对话框"""
    dialog = tk.Toplevel(parent)
    dialog.title("请稍候")
    dialog.geometry("250x100")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()
    
    # 居中显示
    center_window(dialog, 250, 100)
    
    # 创建内容
    frame = ttk.Frame(dialog, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(frame, text=message).pack(pady=(0, 10))
    
    progress = ttk.Progressbar(frame, mode='indeterminate')
    progress.pack(fill=tk.X)
    progress.start()
    
    return dialog
