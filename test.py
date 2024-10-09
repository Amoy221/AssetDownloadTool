#-*-coding:utf-8 -*-
import tkinter as tk
from tkinter import ttk

def show_selected(event):
    branch_name.set(branch_combobox.get())

def print_branch_name():
    print(branch_name.get())

# ��������
window = tk.Tk()

# �����������ѡ��
branch_options = ["Option 1", "Option 2", "Option 3"]

# ���� StringVar ���洢ѡ��ķ�֧��
branch_name = tk.StringVar()

# ���� Combobox ���
branch_combobox = ttk.Combobox(window, values=branch_options, state="readonly", width=13)
branch_combobox.place(x=300, y=20)
branch_combobox.bind("<<ComboboxSelected>>", show_selected)

# ������ť����ӡ branch_name ��ֵ
print_button = tk.Button(window, text="Print branch_name", command=print_branch_name)
print_button.place(x=300, y=50)

window.mainloop()