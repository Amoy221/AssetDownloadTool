#-*-coding:gbk -*-

import tkinter as tk
import requests
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

def download_file(url, file_name):
    with requests.get(url, stream=True) as response:
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        with open(file_name, 'wb') as file:
            for data in tqdm(response.iter_content(block_size), total=total_size // block_size, unit='KB', unit_scale=True):
                if cancel_flag:  # 如果取消标志为真，则停止下载
                    print("Download canceled.")
                    return
                file.write(data)

def cancel_download():
    global cancel_flag
    cancel_flag = True

# 创建GUI窗口
root = tk.Tk()

# 创建一个取消下载的按钮
cancel_button = tk.Button(root, text="Cancel Download", command=cancel_download)
cancel_button.pack()

# 设置取消标志的初始值
cancel_flag = False

# 运行下载代码
manifest_json = 'http://10.11.80.80:81/tgame/DLC23/Android_ASTC/updates/3559.0/' + 'manifest.json'
response_manifest = requests.get(manifest_json)
if response_manifest.status_code == 200:
    data_dict = response_manifest.json()
    paks_list = data_dict['paks']
    assets_url = 'http://10.11.80.80:81/tgame/DLC23/Android_ASTC/updates/3559.0/' + 'assets/'
    response_assets = requests.get(assets_url)
    download_link_list = []
    if response_assets.status_code == 200:
        soup = BeautifulSoup(response_assets.content, 'html.parser')
        download_links = soup.find_all('a')
        for link in download_links:
            download_link = link.get('href')
            download_link_list.append(download_link)
        for download_link in download_link_list[1:]:
            for paks_dict in paks_list:
                if download_link == paks_dict['hash']:
                    file_name = paks_dict['name']
                    download_dir = os.path.join('D:/android', file_name)
                    download_file(assets_url + download_link, download_dir)
else:
    print('Failed to retrieve manifest data:', response_manifest.status_code)

# 运行GUI主循环
root.mainloop()