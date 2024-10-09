#-*-coding:utf-8 -*-
import tkinter as tk
from tkinter import ttk

def show_selected(event):
    branch_name.set(branch_combobox.get())

def print_branch_name():
    print(branch_name.get())

# 创建窗口
window = tk.Tk()

# 定义下拉框的选项
branch_options = ["Option 1", "Option 2", "Option 3"]

# 定义 StringVar 来存储选择的分支名
branch_name = tk.StringVar()

# 创建 Combobox 组件
branch_combobox = ttk.Combobox(window, values=branch_options, state="readonly", width=13)
branch_combobox.place(x=300, y=20)
branch_combobox.bind("<<ComboboxSelected>>", show_selected)

# 创建按钮来打印 branch_name 的值
print_button = tk.Button(window, text="Print branch_name", command=print_branch_name)
print_button.place(x=300, y=50)

window.mainloop()