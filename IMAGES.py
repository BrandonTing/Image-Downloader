import tkinter as tk
import urllib
from bs4 import BeautifulSoup
import os
import requests

def Download():
    baseurl =  input1_value.get()
    PageNumber = input3_value.get()    
    Target_dir = "C:\\Users\\Brandon\\Pictures\\WebScraping" + "\\" + input2_value.get()
    print(Target_dir)    
    urls =[]
    urls.append(baseurl)
    imgID = 0
    #先整理出全部要下載的網頁
    for page in range (2, PageNumber, 1):
        #根據首頁與後面頁面網址的不同做調整
        url = (baseurl + str(page) + ".html")
        urls.append(url)
    for u in urls:
        content = getContentFromUrl(u)
        getInfoFromContent(content, Target_dir, imgID)
        #每頁有五張圖片，但getInfoFromContent函數中增加的imgID並不會傳到這層來，因此到翻頁後要把img ID + 5。
        imgID = imgID + 5
    print("下载成功!")
    

def OpenFolder():
    Target_dir = "C:\\Users\\Brandon\\Pictures\\WebScraping" + "\\" + input2_value.get()
    try:
        os.startfile(Target_dir)
    except:
        #若無此資料夾則不打開
        pass

def getContentFromUrl(url):
    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    proxies = {
            "http": "http://103.252.131.148",
    }
    content = requests.get(url, proxies = proxies, headers = headers).content
    content = BeautifulSoup(content, "html.parser", from_encoding='UTF-8')
    return content

def getInfoFromContent(content, Target_dir, imgID):
    #根據網頁不同調整class/id與名稱
    imgs= content.find_all('img', {"class" : "img"})    
    #若無此資料夾則新建
    if not os.path.isdir(Target_dir):
            os.makedirs(Target_dir)
    for link in imgs: 
        url = link.get('src')
        urllib.request.urlretrieve(url, "%s/img%02d.jpg"% (Target_dir,imgID)) 
        print("正在下載" + link.get('src'))
        imgID = imgID+1

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Image Downloader')
    text1 = tk.Label(root, text = "網址")
    text1.grid(row = 0, column = 0)
    text2 = tk.Label(root, text = "資料夾名稱")
    text2.grid(row = 1, column = 0)
    text3 = tk.Label(root, text = "頁數")
    text3.grid(row = 2, column = 0)

    input1_value=tk.StringVar()
    input1 = tk.Entry(root, textvariable=input1_value)
    input1.grid(row = 0, column = 1)

    input2_value=tk.StringVar()
    input2 = tk.Entry(root, textvariable=input2_value)
    input2.grid(row = 1, column = 1)

    input3_value=tk.IntVar()
    input3 = tk.Entry(root, textvariable=input3_value)
    input3.grid(row = 2, column = 1)

    baseurl =  input1_value.get()
    FolderName = input2_value.get()
    PageNumber = input3_value.get()

    button1=tk.Button(root, text = "下載", command = Download)
    button1.grid(row = 0, column = 2)

    button2=tk.Button(root, text = "打開資料夾", command = OpenFolder)
    button2.grid(row = 1, column = 2)

    root.mainloop()

