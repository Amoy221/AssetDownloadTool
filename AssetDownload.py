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
    # download_links = {
    #     "Option 1": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3258.apk",
    #     "Option 2": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3266.apk",
    #     "Option 3": "http://10.11.80.80:81/tgame/dev/Android_ASTC/packages/Game.Development.3267.apk"
    # }

    download_links = "http://10.11.80.80:81/tgame/"+branch_combobox.get()+system+'packages/'+url_combobox.get()
    print(download_links)
    return download_links

# 下载按钮触发的函数
def start_download():
    selected_version = url_combobox.get() # 获取版本下拉框的参数
    download_link = get_download_link(selected_version)
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
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    # 使用 tqdm 显示下载进度
    with open(file_path, 'wb') as file:
        for data in tqdm(response.iter_content(block_size), total=total_size//block_size, unit='KB', unit_scale=True):
            file.write(data)
 
    # progress_label.config(text="下载完成")
    print(f"File downloaded to: {file_path}")

# 下载按钮
download_button = tk.Button(window,text='下载',width=15,command=start_download)
download_button.place(x=180,y=120)

window.mainloop()