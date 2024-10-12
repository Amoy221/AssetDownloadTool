#-*-coding:gbk -*-

import tkinter as tk
from tkinter import ttk, filedialog
import requests
import os
from tqdm import tqdm
import threading


# def show_version_selected(event):
#     selected_version = url_combobox.get()
    # download_link = get_download_link(selected_version)
    # if download_link:
    #     directory_path = filedialog.askdirectory()
    #     if directory_path:
    #         # download_file(download_link, directory_path)
    #         # 启动下载线程，避免主线程被阻塞，导致窗口无响应
    #         download_thread = threading.Thread(target=download_file, args=(download_link, directory_path))
    #         download_thread.start()

def start_download():
    selected_version = url_combobox.get()
    download_link = get_download_link(selected_version)
    if download_link:
        directory_path = filedialog.askdirectory()
        if directory_path:
            # download_file(download_link, directory_path)
            # 启动下载线程，避免主线程被阻塞，导致窗口无响应
            download_thread = threading.Thread(target=download_file, args=(download_link, directory_path))
            download_thread.start()

def get_download_link(version):
    # 根据选择的版本获取相应的下载链接
    download_links = {
        "Option 1": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3258.apk",
        "Option 2": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3266.apk",
        "Option 3": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3267.apk"
    }
    return download_links.get(version)

def download_file(url, directory):
    # 从给定的 URL 下载文件并保存到指定目录，并显示下载进度
    file_name = url.split('/')[-1]
    file_path = os.path.join(directory, file_name)
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    # 使用 tqdm 显示下载进度
    with open(file_path, 'wb') as file:
        for data in tqdm(response.iter_content(block_size), total=total_size//block_size, unit='KB', unit_scale=True):
            file.write(data)
 
    progress_label.config(text="下载完成")
    print(f"File downloaded to: {file_path}")



# 创建窗口
window = tk.Tk()

# 定义下拉框的选项
version_options = ["Option 1", "Option 2", "Option 3"]

# 创建 Combobox 组件
url_combobox = ttk.Combobox(window, values=version_options, state="readonly", width=30)
url_combobox.place(x=170, y=50)
# url_combobox.bind("<<ComboboxSelected>>", show_version_selected)

start_download_button = tk.Button(window, text="开始下载", command=start_download)
start_download_button.place(x=200, y=80)


# 创建标签用于显示下载进度
progress_label = tk.Label(window, text="未开始")
progress_label.pack()

window.mainloop()