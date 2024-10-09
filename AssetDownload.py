#-*-coding:GBK -*-
import tkinter as tk
from tkinter import ttk
import requests
from  bs4 import BeautifulSoup
from lxml import html
import re



window = tk.Tk()
window.title('CBJQAssetDownload')
window.geometry('600x400') # ���x�߶�


# ��׿��iOS��checkbutton
def print_selection(button_num):  # Ҳ����д�������ص�����
    if button_num == 1:  # ��ѡ�е�һ��checkbutton
        if var2.get() == 1:  # ����ʱ�ڶ���checkbuttonΪѡ��״̬ʱ 
            ios_cb.deselect()
    elif button_num == 2:
        if var1.get() == 1:  
            android_cb.deselect()
        
var1 = tk.IntVar(value=1) # Ĭ��ѡ��
var2 = tk.IntVar()
android_cb = tk.Checkbutton(window,text='Android',variable=var1,onvalue=1,offvalue=0,command=lambda:print_selection(1))
android_cb.place(x=170,y=20)
ios_cb = tk.Checkbutton(window,text='IOS',variable=var2,onvalue=1,offvalue=0,command=lambda:print_selection(2))
ios_cb.place(x=250,y=20)


tk.Label(window,text='���µ�url��').place(x=100,y=50)
tk.Label(window,text='���Ŀ¼��').place(x=100,y=75)

# var_url = tk.StringVar()
# var_url.set('�������url')
# entry_usr_name = tk.Entry(window,textvariable=var_url).place(x=180,y=50)

# �����֧�������ѡ��
branch_options = []

Tgame_url = 'http://10.11.80.80:81/tgame/'
response = requests.get(Tgame_url)
print(response)
if response.status_code == 200:
    soup = BeautifulSoup(response.content,'html.parser') # ������ҳ��Ϣ
    branch = soup.find_all('a') # ��ȡ���е�a��ǩ
    # print(branch)
    for index in range(1,len(branch)):
        # ʹ��lxml����HTML����
        tree = html.fromstring(response.content)
        branch_elements = tree.xpath(f'/html/body/pre/a[{index}]') # ����ֻ�ܻ��[<Element a at 0x2503ea76f20>]
        branch_element = branch_elements[0].text # ��ȡ��ǩ�ڵ��ı�����
        branch_options.append(branch_element)
        # # ʹ��XPath��λ����ʱ����Ϣ������
        # date_elements = tree.xpath(f'/html/body/pre/text()[{index}]')
        # # print(date_elements[0])
        # match = re.search(r'\d{2}-\w{3}-\d{4}\s+(\d{2}:\d{2})', date_elements[0])
        # if match:
        #     date_and_time = match.group(0)
        #     print(branch_element,date_and_time)
        




# ѡ���֧��������
def show_selected(event):
    print(branch_combobox.get())
    global url
    url = Tgame_url+branch_combobox.get()
    print(url)

# # �����������ѡ��
# options = ["Option 1", "Option 2", "Option 3"]
# ���� Combobox ���
branch_combobox = ttk.Combobox(window, values=branch_options, state="readonly", width=13)
branch_combobox.place(x=300,y=20)
branch_combobox.bind("<<ComboboxSelected>>", show_selected)
branch_combobox.current(1) # ������Ĭ��ѡ�е�2��ֵ
url = Tgame_url+branch_combobox.get()
print(url)




# �����������ѡ��
options = ["Option 1", "Option 2", "Option 3"]
# ���� Combobox ���
url_combobox = ttk.Combobox(window, values=options, state="readonly", width=30)
url_combobox.place(x=170,y=50)
url_combobox.bind("<<ComboboxSelected>>", show_selected)


window.mainloop()