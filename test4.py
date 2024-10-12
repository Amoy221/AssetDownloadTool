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
    #         # ���������̣߳��������̱߳����������´�������Ӧ
    #         download_thread = threading.Thread(target=download_file, args=(download_link, directory_path))
    #         download_thread.start()

def start_download():
    selected_version = url_combobox.get()
    download_link = get_download_link(selected_version)
    if download_link:
        directory_path = filedialog.askdirectory()
        if directory_path:
            # download_file(download_link, directory_path)
            # ���������̣߳��������̱߳����������´�������Ӧ
            download_thread = threading.Thread(target=download_file, args=(download_link, directory_path))
            download_thread.start()

def get_download_link(version):
    # ����ѡ��İ汾��ȡ��Ӧ����������
    download_links = {
        "Option 1": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3258.apk",
        "Option 2": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3266.apk",
        "Option 3": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3267.apk"
    }
    return download_links.get(version)

def download_file(url, directory):
    # �Ӹ����� URL �����ļ������浽ָ��Ŀ¼������ʾ���ؽ���
    file_name = url.split('/')[-1]
    file_path = os.path.join(directory, file_name)
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    # ʹ�� tqdm ��ʾ���ؽ���
    with open(file_path, 'wb') as file:
        for data in tqdm(response.iter_content(block_size), total=total_size//block_size, unit='KB', unit_scale=True):
            file.write(data)
 
    progress_label.config(text="�������")
    print(f"File downloaded to: {file_path}")



# ��������
window = tk.Tk()

# �����������ѡ��
version_options = ["Option 1", "Option 2", "Option 3"]

# ���� Combobox ���
url_combobox = ttk.Combobox(window, values=version_options, state="readonly", width=30)
url_combobox.place(x=170, y=50)
# url_combobox.bind("<<ComboboxSelected>>", show_version_selected)

start_download_button = tk.Button(window, text="��ʼ����", command=start_download)
start_download_button.place(x=200, y=80)


# ������ǩ������ʾ���ؽ���
progress_label = tk.Label(window, text="δ��ʼ")
progress_label.pack()

window.mainloop()