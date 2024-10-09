#-*-coding:GBK -*-
import tkinter as tk
from tkinter import ttk
import requests
from  bs4 import BeautifulSoup
from lxml import html
import re



window = tk.Tk()
window.title('CBJQAssetDownload')
window.geometry('600x400') # 宽度x高度


# 安卓和iOS的checkbutton
def print_selection(button_num):  # 也可以写成两个回调函数
    if button_num == 1:  # 当选中第一个checkbutton
        if var2.get() == 1:  # 若此时第二个checkbutton为选中状态时 
            ios_cb.deselect()
    elif button_num == 2:
        if var1.get() == 1:  
            android_cb.deselect()
        
var1 = tk.IntVar(value=1) # 默认选中
var2 = tk.IntVar()
android_cb = tk.Checkbutton(window,text='Android',variable=var1,onvalue=1,offvalue=0,command=lambda:print_selection(1))
android_cb.place(x=170,y=20)
ios_cb = tk.Checkbutton(window,text='IOS',variable=var2,onvalue=1,offvalue=0,command=lambda:print_selection(2))
ios_cb.place(x=250,y=20)


tk.Label(window,text='更新的url：').place(x=100,y=50)
tk.Label(window,text='存放目录：').place(x=100,y=75)

# var_url = tk.StringVar()
# var_url.set('输入更新url')
# entry_usr_name = tk.Entry(window,textvariable=var_url).place(x=180,y=50)

# 定义分支下拉框的选项
branch_options = []

Tgame_url = 'http://10.11.80.80:81/tgame/'
response = requests.get(Tgame_url)
print(response)
if response.status_code == 200:
    soup = BeautifulSoup(response.content,'html.parser') # 解析网页信息
    branch = soup.find_all('a') # 获取所有的a标签
    # print(branch)
    for index in range(1,len(branch)):
        # 使用lxml解析HTML内容
        tree = html.fromstring(response.content)
        branch_elements = tree.xpath(f'/html/body/pre/a[{index}]') # 这里只能获得[<Element a at 0x2503ea76f20>]
        branch_element = branch_elements[0].text # 获取标签内的文本内容
        branch_options.append(branch_element)
        # # 使用XPath定位带有时间信息的链接
        # date_elements = tree.xpath(f'/html/body/pre/text()[{index}]')
        # # print(date_elements[0])
        # match = re.search(r'\d{2}-\w{3}-\d{4}\s+(\d{2}:\d{2})', date_elements[0])
        # if match:
        #     date_and_time = match.group(0)
        #     print(branch_element,date_and_time)
        




# 选择分支的下拉框
def show_selected(event):
    print(branch_combobox.get())
    global url
    url = Tgame_url+branch_combobox.get()
    print(url)

# # 定义下拉框的选项
# options = ["Option 1", "Option 2", "Option 3"]
# 创建 Combobox 组件
branch_combobox = ttk.Combobox(window, values=branch_options, state="readonly", width=13)
branch_combobox.place(x=300,y=20)
branch_combobox.bind("<<ComboboxSelected>>", show_selected)
branch_combobox.current(1) # 下拉框默认选中第2个值
url = Tgame_url+branch_combobox.get()
print(url)




# 定义下拉框的选项
options = ["Option 1", "Option 2", "Option 3"]
# 创建 Combobox 组件
url_combobox = ttk.Combobox(window, values=options, state="readonly", width=30)
url_combobox.place(x=170,y=50)
url_combobox.bind("<<ComboboxSelected>>", show_selected)


window.mainloop()