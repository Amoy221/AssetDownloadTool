#-*-coding:GBK -*-
import tkinter as tk
from tkinter import ttk
import requests
from  bs4 import BeautifulSoup
from lxml import html
import re
from tkinter import filedialog
import threading
import os
from tqdm import tqdm
import subprocess
from tkinter import messagebox

window = tk.Tk()
window.title('CBJQAssetDownload')
window.geometry('600x400') # 宽度x高度

tk.Label(window,text='更新的url：').place(x=100,y=50)
tk.Label(window,text='存放目录：').place(x=100,y=75)

# 定义分支下拉框的选项
branch_options = []
version_options=[]
def spider(url):
    # Tgame_url = 'http://10.11.80.80:81/tgame/'
    
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content,'html.parser') # 解析网页信息
        branch = soup.find_all('a') # 获取所有的a标签
        # print(branch)
        for index in range(1,len(branch)+1):
            # 使用lxml解析HTML内容
            tree = html.fromstring(response.content)
            branch_elements = tree.xpath(f'/html/body/pre/a[{index}]') # 这里只能获得[<Element a at 0x2503ea76f20>]
            branch_element = branch_elements[0].text # 获取标签内的文本内容
            
            if url != 'http://10.11.80.80:81/tgame/':
                version_options.append(branch_element)
                continue        
            branch_options.append(branch_element)
            # # 使用XPath定位带有时间信息的链接
            # date_elements = tree.xpath(f'/html/body/pre/text()[{index}]')
            # # print(date_elements[0])
            # match = re.search(r'\d{2}-\w{3}-\d{4}\s+(\d{2}:\d{2})', date_elements[0])
            # if match:
            #     date_and_time = match.group(0)
            #     print(branch_element,date_and_time)
        print('1')
        print(f'branch_options:{branch_options}')
        print(f'version_options:{version_options}')
    return url

Tgame_url = spider('http://10.11.80.80:81/tgame/')

# 选择分支的下拉框
def show_branch_selected(event):
    print(branch_combobox.get())
    global branch_url
    branch_url = Tgame_url+branch_combobox.get()
    print(branch_url)
    global version_options
    version_options=[] # 再次选中分支时会先清空
    if var1.get() == 1:
        print("android_cb")
        
        spider(branch_url+'Android_ASTC/'+'packages/')
    elif var2.get() == 1:
        print("ios_cb")
        spider(branch_url+'IOS/'+'packages/')
    url_combobox['values'] = version_options   # 更新版本下拉框显示 

# # 定义分支下拉框的选项
# options = ["Option 1", "Option 2", "Option 3"]
# 创建 Combobox 组件
branch_combobox = ttk.Combobox(window, values=branch_options, state="readonly", width=13)
branch_combobox.place(x=300,y=20)
branch_combobox.bind("<<ComboboxSelected>>", show_branch_selected)
branch_combobox.current(1) # 下拉框默认选中第2个值
branch_url = Tgame_url+branch_combobox.get()
print(branch_url)

system = 'Android_ASTC/'
# 安卓和iOS的checkbutton
def print_selection(button_num):  # 也可以写成两个回调函数
    global branch_url
    global version_options
    version_options = [] # 点击时把上一次的列表清空
    global system
    if button_num == 1:  # 当选中第一个checkbutton
        if var2.get() == 1:  # 若此时第二个checkbutton为选中状态时 
            ios_cb.deselect()
        system = 'Android_ASTC/'
    elif button_num == 2:
        if var1.get() == 1:  
            android_cb.deselect()
        system = 'IOS/'
    # print(branch_url+system)
    # spider(branch_url+system+'packages/')
    version_url = branch_url+system+'packages/'
    print(version_url)
    spider(version_url)
    url_combobox['values'] = version_options   # 更新版本下拉框显示 

        
var1 = tk.IntVar(value=1) # 默认选中
var2 = tk.IntVar()
android_cb = tk.Checkbutton(window,text='Android',variable=var1,onvalue=1,offvalue=0,command=lambda:print_selection(1))
android_cb.place(x=170,y=20)
ios_cb = tk.Checkbutton(window,text='IOS',variable=var2,onvalue=1,offvalue=0,command=lambda:print_selection(2))
ios_cb.place(x=250,y=20)

default_version_url = branch_url+android_cb.cget('text')+'_ASTC/packages/'
print(default_version_url)
spider(default_version_url)

# 选择版本的下拉框
def show_version_selected(event):
    print(url_combobox.get())
    
# 定义下拉框的选项
# version_options = ["Option 1", "Option 2", "Option 3"]
# 创建 Combobox 组件
url_combobox = ttk.Combobox(window, values=version_options, state="readonly", width=30)
url_combobox.place(x=170,y=50)
url_combobox.bind("<<ComboboxSelected>>", show_version_selected)

# 设置存放的目录和文件浏览目录按钮
def browse_dirctory():
    directory_path = filedialog.askdirectory(initialdir="/") # 初始化路径
    if directory_path:
        entry_var.set(directory_path)

# 创建Entry组件用于显示和输入目录路径
entry_var = tk.StringVar()
directory_entry = tk.Entry(window,textvariable=entry_var,width=32)
directory_entry.place(x=170,y=80)

# 创建按钮来触发文件浏览目录
browse_button = tk.Button(window,text='Browse',command=browse_dirctory)
browse_button.place(x=400,y=80)

def get_download_link(version):
    # 根据选择的版本获取相应的下载链接
    download_links = "http://10.11.80.80:81/tgame/"+branch_combobox.get()+system+'packages/'+url_combobox.get()
    print(download_links)
    return download_links

# 下载按钮触发的函数
def start_download():

    # 解决url和目录输入框为空还能下载的情况
    if not url_combobox.get():
        tk.messagebox.showwarning(title='Warning',message='请选择要下载的版本')
        return
    if not directory_entry.get():
        tk.messagebox.showwarning(title='Warning',message='请先输入存放的路径')


    # 设置下载标志的初始值
    global Download_flag
    Download_flag = True
    global cancelDownload_flag
    cancelDownload_flag = False
 
    selected_version = url_combobox.get() # 获取版本下拉框的参数
    download_link = get_download_link(selected_version)
    text_widget.configure(state='normal') # 设置文本框为可编辑状态
    if download_link:
        # 启动下载线程，避免主线程被阻塞，导致窗口无响应
        download_thread = threading.Thread(target=download_file, args=(download_link, directory_entry.get()))
        download_thread.start()
    

def download_file(url, directory):
    # 如果指定的文件夹不存在，则创建
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"The directory {directory} has been created.")
    else:
        print(f"The directory {directory} already exists.")

    # 从给定的 URL 下载文件并保存到指定目录，并显示下载进度
    file_name = url.split('/')[-1]
    file_path = os.path.join(directory, file_name)
    response = requests.get(url, stream=True)  # 请求安装包
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    
    text_widget.insert(tk.END, '版本安装包正在下载中.....')  # 将每一行内容插入到文本框中
    text_widget.insert(tk.END, '\n')  # 在插入文本后添加换行符

    # 下载安装包
    # 使用 tqdm 显示下载进度
    with open(file_path, 'wb') as file:
        for data in tqdm(response.iter_content(block_size), total=total_size//block_size, unit='KB', unit_scale=True):
            file.write(data)
 
    # progress_label.config(text="下载完成")
    print(f"File downloaded to: {file_path}")
    print_text = url_combobox.get()+'版本安装包已下载！！！'
    text_widget.insert(tk.END, print_text)  # 将每一行内容插入到文本框中
    text_widget.insert(tk.END, '\n')

    # 下载资源
    
    version_number = re.findall(r'\d+', file_name)
    print(version_number)
    version_number = version_number[0]
    
    version_number = version_number+'.0'
    # 资源的url
    Resources_url = "http://10.11.80.80:81/tgame/"+branch_combobox.get()+system+'updates/'+version_number
    assets_url = Resources_url+'/assets/'
    manifest_json = Resources_url+'/manifest.json'

    # 存放资源的文件夹
    Resources_type_path = system+version_number
    Resources_path = os.path.join(directory, Resources_type_path)
    Resources_path = Resources_path.replace("\\", "/") # 将\反转/
    if not os.path.exists(Resources_path):
        os.makedirs(Resources_path)
    print(f"directory:{directory},Resources_path:{Resources_path}") 

    response_manifest = requests.get(manifest_json)
    if response_manifest.status_code  == 200:
        data_dict = response_manifest.json()
        paks_list = data_dict['paks']
    else:
        print('Failed to retrieve data:', response_manifest.status_code)

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
                print(download_link, paks_dict['name'])
                file_name = paks_dict['name']
                download_dir = os.path.join(Resources_path, file_name)
                with requests.get(assets_url + download_link, stream=True) as response:
                    total_size = int(response.headers.get('content-length', 0))
                    block_size = 1024
                    with open(download_dir, 'wb') as file:
                        for data in tqdm(response.iter_content(block_size), total=total_size // block_size, unit='KB', unit_scale=True):
                            if cancelDownload_flag:  # 如果取消标志为真，则停止下载
                                print("Download canceled.")
                                text_widget.insert(tk.END, "已取消所有下载....")
                                return
                            file.write(data)
                print(f'{file_name}文件已下载')
                # 显示下载内容
                print_text = file_name+'文件已下载'
                text_widget.insert(tk.END, print_text)  # 将每一行内容插入到文本框中
                text_widget.insert(tk.END, '\n')  # 在插入文本后添加换行符
                text_widget.see(tk.END)  # 实时滚动文本框以显示最新内容
    
    print("All files downloaded successfully.")
    text_widget.insert(tk.END, "所有文件下载完成！！！")

# 设置下载标志的初始值
Download_flag = False
# 下载按钮
download_button = tk.Button(window,text='下载',width=15,command=start_download)
download_button.place(x=180,y=120)

# 创建一个文本框
text_widget = tk.Text(window,state='disabled',height=10, width=50) # 设置文本框禁止编辑
text_widget.place(x=100,y=170)

def cancel_download():
    global cancelDownload_flag
    if Download_flag:
        cancelDownload_flag = True

# 设置取消标志的初始值
cancelDownload_flag = False
 
# 创建一个取消下载的按钮
cancel_button = tk.Button(window, text="Cancel Download", command=cancel_download)
cancel_button.place(x=300,y=120)

def open_file_explorer():
    path = directory_entry.get()
    
    if not path:
        print('请先输入存放的路径！')
        tk.messagebox.showwarning(title='Warning',message='请先输入存放的路径！')
    else:
        os.startfile(path) # 打开指定的文件夹

# 添加一个按钮来触发打开文件资源管理器操作
open_explorer_button = tk.Button(window, text="Open File Explorer", command=open_file_explorer)
open_explorer_button.place(x=470,y=170)


window.mainloop()