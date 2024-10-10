#-*-coding:utf-8 -*-
import tkinter as tk
from tkinter import ttk

def update_options():
    if var1.get() == 1:
        branch_combobox['values'] = branch_options1
    else:
        branch_combobox['values'] = branch_options2

# ��������
window = tk.Tk()

# �����������ѡ��
branch_options1 = ["Option 1-1", "Option 1-2", "Option 1-3"]
branch_options2 = ["Option 2-1", "Option 2-2", "Option 2-3"]

# ����Checkbutton���
var1 = tk.IntVar()
checkbutton1 = tk.Checkbutton(window, text="Show List 1", variable=var1, command=update_options)
checkbutton1.pack()

var2 = tk.IntVar()
checkbutton2 = tk.Checkbutton(window, text="Show List 2", variable=var2, command=update_options)
checkbutton2.pack()

# ����Combobox���
branch_combobox = ttk.Combobox(window, state="readonly", width=13)
branch_combobox.pack()

# ��ʼ���������ѡ��
branch_combobox['values'] = branch_options1

window.mainloop()