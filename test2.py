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
    # ����ѡ��İ汾��ȡ��Ӧ����������
    # ���������һ���������ֵ���ӳ��汾����������
    download_links = {
        "Option 1": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3258.apk",
        "Option 2": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3266.apk",
        "Option 3": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3267.apk"
    }
    return download_links.get(version)

def download_file(url, directory):
    # �Ӹ����� URL �����ļ������浽ָ��Ŀ¼
    file_name = url.split('/')[-1]
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'wb') as f:
        response = requests.get(url)
        f.write(response.content)
    print(f"File downloaded to: {file_path}")

# ��������
window = tk.Tk()

# �����������ѡ��
version_options = ["Option 1", "Option 2", "Option 3"]

# ���� Combobox ���
url_combobox = ttk.Combobox(window, values=version_options, state="readonly", width=30)
url_combobox.place(x=170, y=50)
url_combobox.bind("<<ComboboxSelected>>", show_version_selected)

window.mainloop()