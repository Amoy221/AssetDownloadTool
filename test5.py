#-*-coding:gbk -*-
import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

manifest_json = 'http://10.11.80.80:81/tgame/DLC23/Android_ASTC/updates/3559.0/' + 'manifest.json'
print(manifest_json)
response_manifest = requests.get(manifest_json)

if response_manifest.status_code  == 200:
    data_dict = response_manifest.json()
    # print(data_dict)
    # print(type(data_dict['paks']))
    paks_list = data_dict['paks']

else:
    print('Failed to retrieve data:', response_manifest.status_code)


# 从网页中提取下载链接列表
assets_url = 'http://10.11.80.80:81/tgame/DLC23/Android_ASTC/updates/3559.0/' + 'assets/'
print(assets_url)
response_assets = requests.get(assets_url)
download_link_list = []
if response_assets.status_code == 200:
    soup = BeautifulSoup(response_assets.content, 'html.parser')
    download_links = soup.find_all('a')
    for link in download_links:
        download_link = link.get('href')
        download_link_list.append(download_link)

print(download_link_list)
# 遍历下载链接列表，下载文件并显示下载进度
for download_link in download_link_list[1:]:
    for paks_dict in paks_list:
        if download_link == paks_dict['hash']:
            print(download_link, paks_dict['name'])
            file_name = paks_dict['name']
            download_dir = os.path.join('D:/android', file_name)
            with requests.get(assets_url + download_link, stream=True) as response:
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024
                with open(download_dir, 'wb') as file:
                    for data in tqdm(response.iter_content(block_size), total=total_size // block_size, unit='KB', unit_scale=True):
                        file.write(data)
            print(f'{file_name}文件已下载')

print("All files downloaded successfully.")