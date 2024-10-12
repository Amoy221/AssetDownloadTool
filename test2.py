#-*-coding:utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog
import requests
import os

def show_version_selected(event):
    selected_version = url_combobox.get()
    download_link = get_download_link(selected_version)
    if download_link:
        directory_path = filedialog.askdirectory()
        if directory_path:
            download_file(download_link, directory_path)

def get_download_link(version):
    # 根据选择的版本获取相应的下载链接
    # 这里假设有一个函数或字典来映射版本和下载链接
    download_links = {
        "Option 1": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3258.apk",
        "Option 2": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3266.apk",
        "Option 3": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3267.apk"
    }
    return download_links.get(version)

def download_file(url, directory):
    # 从给定的 URL 下载文件并保存到指定目录
    file_name = url.split('/')[-1]
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'wb') as f:
        response = requests.get(url)
        f.write(response.content)
    print(f"File downloaded to: {file_path}")

# 创建窗口
window = tk.Tk()

# 定义下拉框的选项
version_options = ["Option 1", "Option 2", "Option 3"]

# 创建 Combobox 组件
url_combobox = ttk.Combobox(window, values=version_options, state="readonly", width=30)
url_combobox.place(x=170, y=50)
url_combobox.bind("<<ComboboxSelected>>", show_version_selected)

window.mainloop()