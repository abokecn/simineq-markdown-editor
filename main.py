# SPDX-License-Identifier: GPL-3.0
"""
Simineq Markdown Editor v1.0
Copyright (C) 2025 慈父斯大林 <contact@jingsublog.top>
"""
import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from markdown2 import markdown
from tkhtmlview import HTMLLabel


def resource_path(relative_path):
    """ 资源路径处理（用于PyInstaller打包）[6,8](@ref) """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MarkdownEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simineq Markdown Editor")
        self.geometry("1000x600")
        self.current_file = None

        # 初始化界面组件
        self._create_menu()
        self._create_editor()
        self._create_statusbar()
        self._bind_events()

        # 加载默认图标[6](@ref)
        try:
            self.iconbitmap(resource_path('resources/icon.ico'))
        except Exception as e:
            print(f"图标加载失败: {str(e)}")

    def _create_menu(self):
        """ 创建导航栏菜单[1,3](@ref) """
        menubar = tk.Menu(self)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="新建", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="打开", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="保存", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="另存为", command=self.save_as_file)
        menubar.add_cascade(label="文件", menu=file_menu)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)

        self.config(menu=menubar)

    def _create_editor(self):
        """ 创建编辑和预览区域[1,7](@ref) """
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # 编辑区
        self.text_editor = tk.Text(paned, wrap=tk.WORD, font=("Consolas", 12))
        paned.add(self.text_editor, weight=1)

        # 预览区
        self.preview = HTMLLabel(paned, html="<h3>开始编辑...</h3>")
        self.preview.fit_height = True
        paned.add(self.preview, weight=1)

    def _create_statusbar(self):
        """ 状态栏显示操作反馈[7](@ref) """
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _bind_events(self):
        """ 绑定键盘事件[3,8](@ref) """
        self.text_editor.bind("<KeyRelease>", self.update_preview)
        self.bind_all("<Control-n>", lambda e: self.new_file())
        self.bind_all("<Control-s>", lambda e: self.save_file())

    def new_file(self):
        """ 新建Markdown文件[3,8](@ref) """
        if self.text_editor.edit_modified():
            choice = messagebox.askyesnocancel("保存提示", "是否保存当前修改？")
            if choice is None: return
            if choice: self.save_file()

        self.text_editor.delete(1.0, tk.END)
        self.current_file = None
        self.title("未命名文档 - Simineq Markdown Editor")
        self.status_var.set("已创建新文档")

    def open_file(self):
        """ 打开文件对话框[1,7](@ref) """
        file_path = filedialog.askopenfilename(filetypes=[("Markdown文件", "*.md")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.text_editor.delete(1.0, tk.END)
                    self.text_editor.insert(tk.END, f.read())
                self.current_file = file_path
                self.title(f"{os.path.basename(file_path)} - Simineq Markdown Editor")
                self.status_var.set(f"已打开: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"文件读取失败: {str(e)}")

    def save_file(self):
        """ 直接保存文件[3,8](@ref) """
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.text_editor.get(1.0, tk.END))
                self.text_editor.edit_modified(False)
                self.status_var.set(f"已保存到: {self.current_file}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        """ 另存为对话框[1,7](@ref) """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown文件", "*.md"), ("所有文件", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            self.save_file()

    def update_preview(self, event=None):
        """ 实时更新预览[1,7](@ref) """
        content = self.text_editor.get(1.0, tk.END)
        html = markdown(content, extras=["fenced-code-blocks", "tables"])
        self.preview.set_html(html)

    def show_about(self):
        """ 显示关于对话框[3,8](@ref) """
        about_text = """Simineq Markdown Editor v1.0\n
遵循GPL-3.0协议开源\n
作者：慈父斯大林\n
联系方式：contact@jingsublog.top"""
        messagebox.showinfo("关于", about_text)


if __name__ == "__main__":
    app = MarkdownEditor()
    app.mainloop()