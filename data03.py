# https://www.jamleecute.com/python-web-crawler-beautifulsoup-%E7%B6%B2%E8%B7%AF%E7%88%AC%E8%9F%B2/
# 如果先前沒安裝過requests 套件則這邊會失敗, 因此需要先安裝, 可用這個指令: pip install requests
# 載入BeautifulSoup套件, 若沒有的話可以先: pip install beautifulsoup4

import os
import datetime
import sqlite3

import requests
from bs4 import BeautifulSoup

# 指定要抓取的網頁URL
url = 'https://www.ptt.cc/bbs/hotboards.html'
urlbase = 'https://www.ptt.cc'

# 使用requests.get() 來得到網頁回傳內容
r = requests.get(url)
print ('status_code = ', r.status_code) 
# request.get()回傳的是一個物件 
# 若抓成功(即r.status_code==200), 則網頁原始碼會放在物件的text屬性, 我們把它存在一個變數 'web_content'
web_content = r.text
#print(web_content) #可以印出來看看, 會跟從網頁右鍵查看原始碼看到的一樣

# 以 Beautiful Soup 解析 HTML 程式碼 : 
soup = BeautifulSoup(web_content, 'html.parser')
 
boardElements = soup.find_all('a', class_='board')
boardNames = [e.text for e in boardElements]
boardURLs = []
for index in range(len(boardNames)):
    url = urlbase + boardElements[index].get('href')
    boardURLs.append(url)

# 找出所有class為"board-name"的div elements
boardNameElements = soup.find_all('div', class_='board-name')
boardNames = [e.text for e in boardNameElements]
#print(boardNames)

# 觀察網頁原始碼後看到
# 雖然<div class="board-nuser">裡面還有用<span>夾住我們想要的資料(人氣值)
# 不過我們會用.text 直接取出所包含的文字部分即可 
popularityElements = soup.find_all('div', class_="board-nuser")
# 取出的文字的類型是字串, 我們可用int()轉成數字類型
popularities = [int(e.text) for e in popularityElements]

#print(len(boardNames), len(popularities))
# 128 128 == > 一個看板名稱對應一個人氣值, 該PTT頁面共顯示前128個當下最熱門的看板.
 
for pop, bn in zip(popularities, boardNames):
    print(pop, bn)

# 在目前的目錄下尋找一個叫ptt.db的檔案並建立連線, 若不存在則會在你目錄下自動建立這個檔案.
dbPath = 'ptt.db'
dbExist = os.path.exists(dbPath)
if not dbExist:
    connection = sqlite3.connect(dbPath)
    # 後面都用這個 cursor來做SQL操作.
    cursor = connection.cursor()
    sqlstmt = 'CREATE TABLE records (boardnames text, popularity int, url text)'
    cursor.execute(sqlstmt)

    for bn, pop, url in zip(boardNames, popularities, boardURLs):
        cursor.execute('INSERT INTO records VALUES (?,?,?)', (bn, pop, url))
    
    # 將指令送出, 確保前述所有操作已生效
    connection.commit()
    connection.close()